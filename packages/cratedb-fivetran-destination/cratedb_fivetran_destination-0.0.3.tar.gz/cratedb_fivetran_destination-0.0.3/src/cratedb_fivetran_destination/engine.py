import logging
import typing as t

import sqlalchemy as sa
from attr import Factory
from attrs import define
from toolz import dissoc

from cratedb_fivetran_destination.model import FieldMap, SqlBag, TableInfo, TypeMap
from fivetran_sdk import common_pb2

logger = logging.getLogger()


@define
class UpsertStatement:
    """
    Manage and render an SQL upsert statement suitable for CrateDB.

    INSERT INTO ... ON CONFLICT ... DO UPDATE SET ...
    """

    table: TableInfo
    record: t.Dict[str, t.Any] = Factory(dict)

    @property
    def data(self):
        """
        The full record without primary key data.
        """
        return dissoc(self.record, *self.table.primary_keys)

    def to_sql(self) -> SqlBag:
        """
        Render statement to SQL.
        """
        return SqlBag().add(f"""
        INSERT INTO {self.table.fullname}
        ({", ".join([f'"{key}"' for key in self.record.keys()])})
        VALUES ({", ".join([f":{key}" for key in self.record.keys()])})
        ON CONFLICT ({", ".join(self.table.primary_keys)}) DO UPDATE
        SET {", ".join([f'"{key}"="excluded"."{key}"' for key in self.data.keys()])}
        """)  # noqa: S608


@define
class UpdateStatement:
    """
    Manage and render an SQL update statement.

    UPDATE ... SET ... WHERE ...
    """

    table: TableInfo
    record: t.Dict[str, t.Any] = Factory(dict)

    @property
    def data(self):
        """
        The full record without primary key data.
        """
        return dissoc(self.record, *self.table.primary_keys)

    def to_sql(self) -> SqlBag:
        """
        Render statement to SQL.
        """
        return SqlBag().add(f"""
        UPDATE {self.table.fullname}
        SET {", ".join([f'"{key}" = :{key}' for key in self.data.keys()])}
        WHERE {" AND ".join([f'"{key}" = :{key}' for key in self.table.primary_keys])}
        """)  # noqa: S608


@define
class DeleteStatement:
    """
    Manage and render an SQL delete statement.

    DELETE FROM ... WHERE ...
    """

    table: TableInfo
    record: t.Dict[str, t.Any] = Factory(dict)

    def to_sql(self) -> SqlBag:
        """
        Render statement to SQL.
        """
        return SqlBag().add(f"""
        DELETE FROM {self.table.fullname}
        WHERE {" AND ".join([f'"{key}" = :{key}' for key in self.table.primary_keys])}
        """)  # noqa: S608


@define
class AlterTableInplaceStatements:
    """
    Manage and render a procedure of SQL statements for altering/migrating a table schema.
    """

    table: TableInfo
    columns_new: t.List[common_pb2.Column] = Factory(list)
    columns_changed: t.List[common_pb2.Column] = Factory(list)

    def to_sql(self) -> SqlBag:
        sqlbag = SqlBag()

        if not self.columns_new and not self.columns_changed:
            return sqlbag

        # Translate "columns changed" instructions into migration operation
        # based on altering and copying using `UPDATE ... SET ...`.
        for column in self.columns_changed:
            column_name = FieldMap.to_cratedb(column.name)
            column_name_temporary = column_name + "_alter_tmp"
            type_ = TypeMap.to_cratedb(column.type, column.params)
            sqlbag.add(
                f'ALTER TABLE {self.table.fullname} ADD COLUMN "{column_name_temporary}" {type_};'
            )
            sqlbag.add(
                f'UPDATE {self.table.fullname} SET "{column_name_temporary}" = "{column_name}"::{type_};'  # noqa: S608, E501
            )
            sqlbag.add(f'ALTER TABLE {self.table.fullname} DROP "{column_name}";')
            sqlbag.add(
                f'ALTER TABLE {self.table.fullname} RENAME "{column_name_temporary}" TO "{column_name}";'  # noqa: E501
            )

        # Translate "new column" instructions into `ALTER TABLE ... ADD ...` clauses.
        if self.columns_new:
            alter_add_ops: t.List[str] = []
            for column in self.columns_new:
                alter_add_ops.append(f"ADD {self.column_definition(column)}")
            sqlbag.add(f"ALTER TABLE {self.table.fullname} {', '.join(alter_add_ops)};")

        return sqlbag

    @staticmethod
    def column_definition(column):
        field = FieldMap.to_cratedb(column.name)
        type_ = TypeMap.to_cratedb(column.type, column.params)
        return f"{field} {type_}"


@define
class Processor:
    engine: sa.Engine

    def process(
        self,
        table_info: TableInfo,
        upsert_records: t.Generator[t.Dict[str, t.Any], None, None],
        update_records: t.Generator[t.Dict[str, t.Any], None, None],
        delete_records: t.Generator[t.Dict[str, t.Any], None, None],
    ):
        with self.engine.connect() as connection:
            # Apply upsert SQL statements.
            # `INSERT INTO ... ON CONFLICT ... DO UPDATE SET ...`.
            self.process_records(
                connection,
                upsert_records,
                lambda record: UpsertStatement(table=table_info, record=record).to_sql(),
            )

            self.process_records(
                connection,
                update_records,
                lambda record: UpdateStatement(table=table_info, record=record).to_sql(),
            )

            self.process_records(
                connection,
                delete_records,
                lambda record: DeleteStatement(table=table_info, record=record).to_sql(),
            )

    def process_records(self, connection, records, converter):
        for record in records:
            # DML statements are always singular, because they are accompanied with a `record`.
            sql = converter(record).statements[0]
            try:
                connection.execute(sa.text(sql), record)
            except sa.exc.ProgrammingError as ex:
                logger.error(f"Processing database operation failed: {ex}")
                raise
