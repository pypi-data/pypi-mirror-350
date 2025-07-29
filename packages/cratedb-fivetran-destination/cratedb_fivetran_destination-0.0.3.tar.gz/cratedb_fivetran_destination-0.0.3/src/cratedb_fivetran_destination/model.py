import typing as t
from textwrap import dedent

import sqlalchemy as sa
from attr import Factory
from attrs import define
from sqlalchemy_cratedb import ObjectType

from cratedb_fivetran_destination.dictx import OrderedDictX
from fivetran_sdk import common_pb2
from fivetran_sdk.common_pb2 import DataType


class FieldMap:
    """
    Manage special knowledge about CrateDB field names.
    """

    # Map special column names, because CrateDB does not allow `_` prefixes.
    field_map = {
        "_fivetran_id": "__fivetran_id",
        "_fivetran_synced": "__fivetran_synced",
        "_fivetran_deleted": "__fivetran_deleted",
    }

    @classmethod
    def rename_keys(cls, record):
        """
        Rename keys according to the field map.
        """
        record = OrderedDictX(record)
        for key, value in cls.field_map.items():
            if key in record:
                record.rename_key(key, value)
        return record

    @classmethod
    def to_cratedb(cls, fivetran_field):
        """
        Convert a Fivetran field name into a CrateDB field name.
        """
        return cls.field_map.get(fivetran_field, fivetran_field)

    @classmethod
    def to_fivetran(cls, cratedb_field):
        """
        Convert a CrateDB field name into a Fivetran field name.
        """
        # TODO: Compute reverse map only once.
        reverse_map = dict(zip(cls.field_map.values(), cls.field_map.keys()))
        return reverse_map.get(cratedb_field, cratedb_field)


class TypeMap:
    """
    Map Fivetran types to CrateDB types and back.
    """

    cratedb_default = sa.Text()
    fivetran_default = DataType.UNSPECIFIED

    fivetran_map = {
        DataType.UNSPECIFIED: sa.Text(),
        DataType.BOOLEAN: sa.Boolean(),
        DataType.SHORT: sa.SmallInteger(),
        DataType.INT: sa.Integer(),
        DataType.LONG: sa.BigInteger(),
        DataType.FLOAT: sa.Float(),
        DataType.DOUBLE: sa.Double(),
        DataType.NAIVE_DATE: sa.Date(),
        DataType.NAIVE_DATETIME: sa.TIMESTAMP(),
        DataType.UTC_DATETIME: sa.TIMESTAMP(),
        DataType.DECIMAL: sa.DECIMAL(),
        DataType.BINARY: sa.Text(),
        DataType.STRING: sa.String(),
        DataType.JSON: ObjectType,
        DataType.XML: sa.String(),
        DataType.NAIVE_TIME: sa.TIMESTAMP(),
    }

    cratedb_map = {
        sa.Text: DataType.STRING,
        sa.TEXT: DataType.STRING,
        sa.VARCHAR: DataType.STRING,
        sa.Boolean: DataType.BOOLEAN,
        sa.BOOLEAN: DataType.BOOLEAN,
        sa.SmallInteger: DataType.SHORT,
        sa.Integer: DataType.INT,
        sa.BigInteger: DataType.LONG,
        sa.SMALLINT: DataType.SHORT,
        sa.INTEGER: DataType.INT,
        sa.BIGINT: DataType.LONG,
        sa.Float: DataType.FLOAT,
        sa.FLOAT: DataType.FLOAT,
        sa.Double: DataType.DOUBLE,
        sa.DOUBLE: DataType.DOUBLE,
        sa.DOUBLE_PRECISION: DataType.DOUBLE,
        sa.Date: DataType.NAIVE_DATE,
        sa.DATE: DataType.NAIVE_DATE,
        # FIXME: Which one to choose?
        #        Need better inspection about aware/unaware datetime objects?
        # sa.DateTime: DataType.NAIVE_DATETIME,
        sa.DateTime: DataType.UTC_DATETIME,
        sa.DATETIME: DataType.UTC_DATETIME,
        sa.Numeric: DataType.DECIMAL,
        sa.DECIMAL: DataType.DECIMAL,
        sa.LargeBinary: DataType.BINARY,
        sa.BINARY: DataType.BINARY,
        ObjectType: DataType.JSON,
        # FIXME: What about Arrays?
    }

    @classmethod
    def to_cratedb(cls, fivetran_type, fivetran_params=None):
        """
        Convert a Fivetran type into a CrateDB type.
        """
        # TODO: Introduce parameter handling to type mappers.
        return cls.fivetran_map.get(fivetran_type, cls.cratedb_default)

    @classmethod
    def to_fivetran(cls, cratedb_type):
        """
        Convert a CrateDB type into a Fivetran type.
        """
        return cls.cratedb_map.get(type(cratedb_type), cls.fivetran_default)


class FivetranKnowledge:
    """
    Manage special knowledge about Fivetran.

    Fivetran uses special values for designating NULL and CDC-unmodified values.
    """

    NULL_STRING = "null-m8yilkvPsNulehxl2G6pmSQ3G3WWdLP"
    UNMODIFIED_STRING = "unmod-NcK9NIjPUutCsz4mjOQQztbnwnE1sY3"

    @classmethod
    def replace_values(cls, record):
        rm_list = []
        for key, value in record.items():
            if value == cls.NULL_STRING:
                record[key] = None
            elif value == cls.UNMODIFIED_STRING:
                rm_list.append(key)
        for rm in rm_list:
            record.pop(rm)


@define
class TableInfo:
    """
    Manage information about a database table.
    """

    fullname: str
    primary_keys: t.List[str] = Factory(list)


@define
class SqlBag:
    """
    A little bag of multiple SQL statements.
    """

    statements: t.List[str] = Factory(list)

    def __bool__(self):
        return bool(self.statements)

    def add(self, sql: str):
        self.statements.append(dedent(sql).strip())
        return self

    def execute(self, connection: sa.Connection):
        for sql in self.statements:
            connection.execute(sa.text(sql))


class FivetranTable:
    """Provide helper methods for Fivetran tables."""

    @classmethod
    def pk_column_names(cls, table: common_pb2.Table) -> t.List[str]:
        """Return list of primary keys column names."""
        return [column.name for column in table.columns if column.primary_key]

    @classmethod
    def pk_equals(cls, t1: common_pb2.Table, t2: common_pb2.Table) -> bool:
        """Return whether two tables have the same primary keys."""
        return cls.pk_column_names(t1) == cls.pk_column_names(t2)
