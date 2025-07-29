# ruff: noqa: S608  # Possible SQL injection vector through string-based query construction
# Source: https://github.com/fivetran/fivetran_sdk/tree/v2/examples/destination_connector/python
import logging
import typing as t
from concurrent import futures

import grpc
import sqlalchemy as sa

from cratedb_fivetran_destination.engine import AlterTableInplaceStatements, Processor
from cratedb_fivetran_destination.model import (
    FieldMap,
    FivetranKnowledge,
    FivetranTable,
    TableInfo,
    TypeMap,
)
from cratedb_fivetran_destination.util import LOG_INFO, LOG_SEVERE, LOG_WARNING, log_message
from fivetran_sdk import common_pb2, destination_sdk_pb2, destination_sdk_pb2_grpc

from . import read_csv

logger = logging.getLogger()


class CrateDBDestinationImpl(destination_sdk_pb2_grpc.DestinationConnectorServicer):
    def __init__(self):
        self.metadata = sa.MetaData()
        self.engine: sa.Engine = None
        self.processor: Processor = None

    def ConfigurationForm(self, request, context):
        log_message(LOG_INFO, "Fetching configuration form")

        # Create the form fields.
        form_fields = common_pb2.ConfigurationFormResponse(
            schema_selection_supported=True, table_selection_supported=True
        )

        # SQLAlchemy database connection URL.
        url = common_pb2.FormField(
            name="url",
            label="CrateDB database connection URL in SQLAlchemy format",
            text_field=common_pb2.TextField.PlainText,
            placeholder="crate://<username>:<password>@example.gke1.us-central1.gcp.cratedb.net:4200?ssl=true",
            default_value="crate://",
        )

        # Add fields to the form.
        form_fields.fields.append(url)

        # Add tests to the form.
        form_fields.tests.add(name="connect", label="Tests connection")
        # TODO: How to invoke this test?
        form_fields.tests.add(name="select", label="Tests selection")

        return form_fields

    def Test(self, request, context):
        """
        Verify database connectivity with configured connection parameters.
        """
        log_message(LOG_INFO, f"Test database connection: {request.name}")
        self._configure_database(request.configuration.get("url"))
        with self.engine.connect() as connection:
            connection.execute(sa.text("SELECT 42"))
        return common_pb2.TestResponse(success=True)

    def CreateTable(self, request, context):
        """
        Create database table using SQLAlchemy.
        """
        self._configure_database(request.configuration.get("url"))
        logger.info(
            "[CreateTable] :"
            + str(request.schema_name)
            + " | "
            + str(request.table.name)
            + " | "
            + str(request.table.columns)
        )
        table = sa.Table(request.table.name, self.metadata, schema=request.schema_name)
        fivetran_column: common_pb2.Column
        for fivetran_column in request.table.columns:
            db_column: sa.Column = sa.Column()
            db_column.name = FieldMap.to_cratedb(fivetran_column.name)
            db_column.type = TypeMap.to_cratedb(fivetran_column.type)
            db_column.primary_key = fivetran_column.primary_key
            if db_column.primary_key:
                db_column.nullable = False
            # TODO: Which kind of parameters are relayed by Fivetran here?
            # db_column.params(fivetran_column.params)  # noqa: ERA001
            table.append_column(db_column)

        # Need to add the `__fivetran_deleted` column manually?
        col: sa.Column = sa.Column(name="__fivetran_deleted")
        col.type = sa.Boolean()
        table.append_column(col)

        table.create(self.engine)
        return destination_sdk_pb2.CreateTableResponse(success=True)

    def AlterTable(self, request, context):
        """
        Alter schema of database table.
        """
        self._configure_database(request.configuration.get("url"))
        res: destination_sdk_pb2.AlterTableResponse  # noqa: F842
        logger.info(
            "[AlterTable]: "
            + str(request.schema_name)
            + " | "
            + str(request.table.name)
            + " | "
            + str(request.table.columns)
        )

        # Compute schema diff.
        old_table = self.DescribeTable(request, context).table
        new_table = request.table

        pk_has_changed = False
        if not FivetranTable.pk_equals(old_table, new_table):
            pk_has_changed = True

        columns_old: t.Dict[str, common_pb2.Column] = {
            column.name: column for column in old_table.columns
        }

        columns_new: t.List[common_pb2.Column] = []
        columns_changed: t.List[common_pb2.Column] = []
        columns_common: t.List[common_pb2.Column] = []

        for column in new_table.columns:
            column_old = columns_old.get(column.name)
            if column_old is None:
                columns_new.append(column)
            else:
                columns_common.append(column)
                type_old = TypeMap.to_cratedb(column_old.type, column_old.params)
                type_new = TypeMap.to_cratedb(column.type, column.params)
                if type_old != type_new:
                    if column_old.primary_key:
                        pk_has_changed = True
                        continue

                    columns_changed.append(column)

        table_info = self._table_info_from_request(request)
        if pk_has_changed:
            log_message(
                LOG_WARNING,
                "Alter table intends to change the primary key of the table. "
                "Because CrateDB does not support this operation, the table will be recreated.",
            )
            # FIXME: Implement non-inplace ALTER TABLE for primary key updates.
            """
            ats = AlterTableRecreateStatements(
                table=table_info, table_new=new_table, columns_common=columns_common
            )
            """
            msg = (
                "Alter table intends to change the primary key of the table, "
                "but this operation is not implemented yet"
            )
            log_message(LOG_SEVERE, f"AlterTable: {msg}")
            return destination_sdk_pb2.AlterTableResponse(
                success=False,
                warning=common_pb2.Warning(message=msg),
            )
        ats = AlterTableInplaceStatements(
            table=table_info, columns_new=columns_new, columns_changed=columns_changed
        )
        with self.engine.connect() as connection:
            stmts = ats.to_sql()
            if stmts:
                stmts.execute(connection)
                log_message(
                    LOG_INFO, f"AlterTable: Successfully altered table: {table_info.fullname}"
                )
            else:
                log_message(LOG_INFO, "AlterTable: Nothing changed")

        return destination_sdk_pb2.AlterTableResponse(success=True)

    def Truncate(self, request, context):
        """
        Truncate database table.
        """
        self._configure_database(request.configuration.get("url"))
        logger.info(
            "[TruncateTable]: "
            + str(request.schema_name)
            + " | "
            + str(request.table_name)
            + " | soft"
            + str(request.soft)
        )
        with self.engine.connect() as connection:
            connection.execute(sa.text(f"DELETE FROM {self.table_fullname(request)}"))
        return destination_sdk_pb2.TruncateResponse(success=True)

    def WriteBatch(self, request, context):
        """
        Upsert records using SQL.
        """
        self._configure_database(request.configuration.get("url"))
        table_info = self._table_info_from_request(request)
        log_message(LOG_INFO, f"Data loading started for table: {request.table.name}")
        self.processor.process(
            table_info=table_info,
            upsert_records=self._files_to_records(request, request.replace_files),
            update_records=self._files_to_records(request, request.update_files),
            delete_records=self._files_to_records(request, request.delete_files),
        )
        log_message(LOG_INFO, f"Data loading completed for table: {request.table.name}")

        res: destination_sdk_pb2.WriteBatchResponse = destination_sdk_pb2.WriteBatchResponse(
            success=True
        )
        return res

    def DescribeTable(self, request, context):
        """
        Reflect table schema using SQLAlchemy.
        """
        self._configure_database(request.configuration.get("url"))
        table_name = self.table_name(request)
        table: common_pb2.Table = common_pb2.Table(name=table_name)
        try:
            sa_table = self._reflect_table(schema=request.schema_name, table=table_name)
        except sa.exc.NoSuchTableError:
            msg = f"Table not found: {table_name}"
            log_message(LOG_WARNING, f"DescribeTable: {msg}")
            return destination_sdk_pb2.DescribeTableResponse(
                not_found=True, table=table, warning=common_pb2.Warning(message=msg)
            )
        sa_column: sa.Column
        for sa_column in sa_table.columns:
            ft_column = common_pb2.Column(
                name=FieldMap.to_fivetran(sa_column.name),
                type=TypeMap.to_fivetran(sa_column.type),
                primary_key=sa_column.primary_key,
            )
            table.columns.append(ft_column)
        log_message(LOG_INFO, f"Completed fetching table info: {table}")
        return destination_sdk_pb2.DescribeTableResponse(not_found=False, table=table)

    def _configure_database(self, url):
        if not self.engine:
            self.engine = sa.create_engine(url)
            self.processor = Processor(engine=self.engine)

    @staticmethod
    def _files_to_records(request, files: t.List[str]):
        """
        Decrypt payload files and generate records.
        """
        for filename in files:
            value = request.keys[filename]
            logger.info(f"Decrypting file: {filename}")
            for record in read_csv.decrypt_file(filename, value):
                # Rename keys according to field map.
                record = FieldMap.rename_keys(record)
                FivetranKnowledge.replace_values(record)
                yield record

    def _reflect_table(self, schema: str, table: str):
        """
        Acquire table schema from database.
        """
        return sa.Table(
            table,
            self.metadata,
            schema=schema,
            quote_schema=True,
            autoload_with=self.engine,
        )

    def _table_info_from_request(self, request) -> TableInfo:
        """
        Compute TableInfo data.
        """
        table = self._reflect_table(schema=request.schema_name, table=request.table.name)
        primary_keys = [column.name for column in table.primary_key.columns]
        return TableInfo(fullname=self.table_fullname(request), primary_keys=primary_keys)

    @staticmethod
    def table_name(request):
        """
        Return table name from request object.
        """
        if hasattr(request, "table"):
            return request.table.name
        return request.table_name

    def table_fullname(self, request):
        """
        Return full-qualified table name from request object.
        """
        table_name = self.table_name(request)
        return f'"{request.schema_name}"."{table_name}"'


def start_server(host: str = "[::]", port: int = 50052, max_workers: int = 1) -> grpc.Server:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    server.add_insecure_port(f"{host}:{port}")
    destination_sdk_pb2_grpc.add_DestinationConnectorServicer_to_server(
        CrateDBDestinationImpl(), server
    )
    server.start()
    return server
