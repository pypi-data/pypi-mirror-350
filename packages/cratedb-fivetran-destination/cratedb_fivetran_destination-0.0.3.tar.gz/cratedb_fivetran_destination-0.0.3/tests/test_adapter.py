import re

import pytest
import sqlalchemy as sa

from cratedb_fivetran_destination import __version__
from cratedb_fivetran_destination.engine import Processor
from cratedb_fivetran_destination.model import TableInfo
from cratedb_fivetran_destination.util import format_log_message, setup_logging
from fivetran_sdk import common_pb2, destination_sdk_pb2


def test_version():
    assert __version__ >= "0.0.0"


def test_setup_logging():
    setup_logging(verbose=True)


def test_api_test(capsys):
    """
    Invoke gRPC API method `Test`.
    """
    from cratedb_fivetran_destination.main import CrateDBDestinationImpl

    destination = CrateDBDestinationImpl()

    # Invoke gRPC API method.
    config = {"url": "crate://"}
    response = destination.Test(
        request=common_pb2.TestRequest(name="foo", configuration=config),
        context=common_pb2.TestResponse(),
    )

    # Validate outcome.
    assert response.success is True
    assert response.failure == ""

    # Check log output.
    out, err = capsys.readouterr()
    assert out == format_log_message("Test database connection: foo", newline=True)


def test_api_configuration_form(capsys):
    """
    Invoke gRPC API method `ConfigurationForm`.
    """
    from cratedb_fivetran_destination.main import CrateDBDestinationImpl

    destination = CrateDBDestinationImpl()

    # Invoke gRPC API method.
    response = destination.ConfigurationForm(
        request=common_pb2.ConfigurationFormRequest(),
        context=common_pb2.ConfigurationFormResponse(),
    )

    # Extract field of concern.
    url_field: common_pb2.FormField = response.fields[0]

    # Validate fields.
    assert url_field.name == "url"
    assert "CrateDB database connection URL" in url_field.label

    # Validate tests.
    assert response.tests[0].name == "connect"

    # Check log output.
    out, err = capsys.readouterr()
    assert out == format_log_message("Fetching configuration form", newline=True)


def test_api_describe_table_found(engine, capsys):
    """
    Invoke gRPC API method `DescribeTable` on an existing table.
    """
    from cratedb_fivetran_destination.main import CrateDBDestinationImpl

    destination = CrateDBDestinationImpl()

    with engine.connect() as conn:
        conn.execute(sa.text("DROP TABLE IF EXISTS testdrive.foo"))
        conn.execute(sa.text("CREATE TABLE testdrive.foo (id INT)"))

    # Invoke gRPC API method under test.
    config = {"url": "crate://"}
    response = destination.DescribeTable(
        request=destination_sdk_pb2.DescribeTableRequest(
            table_name="foo", schema_name="testdrive", configuration=config
        ),
        context=destination_sdk_pb2.DescribeTableResponse(),
    )

    # Validate outcome.
    assert response.not_found is False
    assert response.warning.message == ""
    assert response.table == common_pb2.Table(
        name="foo",
        columns=[
            common_pb2.Column(
                name="id",
                type=common_pb2.DataType.INT,
                primary_key=False,
            )
        ],
    )

    # Check log output.
    out, err = capsys.readouterr()
    assert "Completed fetching table info" in out


def test_api_describe_table_not_found(capsys):
    """
    Invoke gRPC API method `DescribeTable` on an existing table.
    """
    from cratedb_fivetran_destination.main import CrateDBDestinationImpl

    destination = CrateDBDestinationImpl()

    # Invoke gRPC API method under test.
    config = {"url": "crate://"}
    response = destination.DescribeTable(
        request=destination_sdk_pb2.DescribeTableRequest(
            table_name="unknown", schema_name="testdrive", configuration=config
        ),
        context=destination_sdk_pb2.DescribeTableResponse(),
    )

    # Validate outcome.
    assert response.not_found is False
    assert response.warning.message == "Table not found: unknown"
    assert response.table.name == ""
    assert response.table.columns == []

    # Check log output.
    out, err = capsys.readouterr()
    assert out == format_log_message(
        "DescribeTable: Table not found: unknown", level="WARNING", newline=True
    )


def test_api_alter_table_add_column(engine, capsys):
    """
    Invoke gRPC API method `AlterTable`, adding a new column.
    """
    from cratedb_fivetran_destination.main import CrateDBDestinationImpl

    destination = CrateDBDestinationImpl()

    with engine.connect() as conn:
        conn.execute(sa.text("DROP TABLE IF EXISTS testdrive.foo"))
        conn.execute(sa.text("CREATE TABLE testdrive.foo (id INT)"))

    # Invoke gRPC API method under test.
    table: common_pb2.Table = common_pb2.Table(name="foo")
    column: common_pb2.Column = common_pb2.Column(
        name="bar",
        type=common_pb2.DataType.STRING,
        primary_key=False,
    )
    table.columns.append(column)
    config = {"url": "crate://"}
    response = destination.AlterTable(
        request=destination_sdk_pb2.AlterTableRequest(
            table=table, schema_name="testdrive", configuration=config
        ),
        context=destination_sdk_pb2.AlterTableResponse(),
    )

    # Validate outcome.
    assert response.success is True
    assert response.warning.message == ""

    # Check log output.
    out, err = capsys.readouterr()
    assert (
        format_log_message(
            'AlterTable: Successfully altered table: "testdrive"."foo"', newline=True
        )
        in out
    )


def test_api_alter_table_nothing_changed(engine, capsys):
    """
    Invoke gRPC API method `AlterTable`, but nothing changed.
    """
    from cratedb_fivetran_destination.main import CrateDBDestinationImpl

    destination = CrateDBDestinationImpl()

    with engine.connect() as conn:
        conn.execute(sa.text("DROP TABLE IF EXISTS testdrive.foo"))
        conn.execute(sa.text("CREATE TABLE testdrive.foo (id INT)"))

    # Invoke gRPC API method under test.
    table: common_pb2.Table = common_pb2.Table(
        name="foo",
        columns=[
            common_pb2.Column(
                name="id",
                type=common_pb2.DataType.INT,
                primary_key=False,
            )
        ],
    )
    config = {"url": "crate://"}
    response = destination.AlterTable(
        request=destination_sdk_pb2.AlterTableRequest(
            table=table, schema_name="testdrive", configuration=config
        ),
        context=destination_sdk_pb2.AlterTableResponse(),
    )

    # Validate outcome.
    assert response.success is True
    assert response.warning.message == ""

    # Check log output.
    out, err = capsys.readouterr()
    assert format_log_message("AlterTable: Nothing changed", newline=True) in out


def test_api_alter_table_change_primary_key_type(engine, capsys):
    """
    Invoke gRPC API method `AlterTable`, changing the type of the primary key.
    """
    from cratedb_fivetran_destination.main import CrateDBDestinationImpl

    destination = CrateDBDestinationImpl()

    with engine.connect() as conn:
        conn.execute(sa.text("DROP TABLE IF EXISTS testdrive.foo"))
        conn.execute(sa.text("CREATE TABLE testdrive.foo (id INT PRIMARY KEY)"))

    # Invoke gRPC API method under test.
    table: common_pb2.Table = common_pb2.Table(name="foo")
    column: common_pb2.Column = common_pb2.Column(
        name="id",
        type=common_pb2.DataType.STRING,
        primary_key=True,
    )
    table.columns.append(column)
    config = {"url": "crate://"}
    response = destination.AlterTable(
        request=destination_sdk_pb2.AlterTableRequest(
            table=table, schema_name="testdrive", configuration=config
        ),
        context=destination_sdk_pb2.AlterTableResponse(),
    )

    # Validate outcome.
    assert response.success is False
    assert "this operation is not implemented yet" in response.warning.message

    # Check log output.
    out, err = capsys.readouterr()
    # assert out == format_log_message("AlterTable: Successfully altered table: ", newline=True)  # noqa: E501, ERA001
    assert "this operation is not implemented yet" in out


def test_api_alter_table_change_primary_key_name(engine, capsys):
    """
    Invoke gRPC API method `AlterTable`, changing the name of the primary key.
    """
    from cratedb_fivetran_destination.main import CrateDBDestinationImpl

    destination = CrateDBDestinationImpl()

    with engine.connect() as conn:
        conn.execute(sa.text("DROP TABLE IF EXISTS testdrive.foo"))
        conn.execute(sa.text("CREATE TABLE testdrive.foo (id INT PRIMARY KEY)"))

    # Invoke gRPC API method under test.
    table: common_pb2.Table = common_pb2.Table(name="foo")
    column: common_pb2.Column = common_pb2.Column(
        name="identfier",
        type=common_pb2.DataType.INT,
        primary_key=True,
    )
    table.columns.append(column)
    config = {"url": "crate://"}
    response = destination.AlterTable(
        request=destination_sdk_pb2.AlterTableRequest(
            table=table, schema_name="testdrive", configuration=config
        ),
        context=destination_sdk_pb2.AlterTableResponse(),
    )

    # Validate outcome.
    assert response.success is False
    assert "this operation is not implemented yet" in response.warning.message

    # Check log output.
    out, err = capsys.readouterr()
    # assert out == format_log_message("AlterTable: Successfully altered table: ", newline=True)  # noqa: E501, ERA001
    assert "this operation is not implemented yet" in out


def test_processor_failing(engine):
    table_info = TableInfo(fullname="unknown.unknown", primary_keys=["id"])
    p = Processor(engine=engine)
    with pytest.raises(sa.exc.ProgrammingError) as ex:
        p.process(
            table_info=table_info,
            upsert_records=[{"id": 1, "name": "Hotzenplotz"}],
            update_records=[{"id": 2}],
            delete_records=[{"id": 2}],
        )
    assert ex.match(re.escape("SchemaUnknownException[Schema 'unknown' unknown]"))
