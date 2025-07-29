import subprocess
import threading
from textwrap import dedent
from time import sleep
from unittest import mock

import pytest
import sqlalchemy as sa
from sqlalchemy.sql.type_api import UserDefinedType
from sqlalchemy_cratedb import ObjectType


def run(command: str, background: bool = False):
    if background:
        return subprocess.Popen(command, shell=True)  # noqa: S602
    subprocess.check_call(command, stderr=subprocess.STDOUT, shell=True)  # noqa: S602
    return None


@pytest.fixture(autouse=True)
def reset_tables(engine):
    with engine.connect() as connection:
        connection.execute(sa.text("DROP TABLE IF EXISTS tester.all_types"))
        connection.execute(sa.text("DROP TABLE IF EXISTS tester.campaign"))
        connection.execute(sa.text("DROP TABLE IF EXISTS tester.transaction"))


@pytest.fixture()
def services(request):
    """
    Invoke the CrateDB Fivetran destination gRPC adapter and the Fivetran destination tester.
    """
    data_folder = request.param

    processes = []

    oci_image = (
        "us-docker.pkg.dev/build-286712/public-docker-us/sdktesters-v2/sdk-tester:2.25.0131.001"
    )
    run("gcloud auth configure-docker us-docker.pkg.dev")
    run(f"docker pull {oci_image}")

    # Start gRPC server.
    from cratedb_fivetran_destination.main import start_server

    server = None

    def starter():
        nonlocal server
        server = start_server()

    t = threading.Thread(target=starter)
    t.start()

    cmd = dedent(f"""
    docker run --rm \
      --mount type=bind,source={data_folder},target=/data \
      -a STDIN -a STDOUT -a STDERR \
      -e WORKING_DIR={data_folder} \
      -e GRPC_HOSTNAME=host.docker.internal \
      --network=host \
      --add-host=host.docker.internal:host-gateway \
      {oci_image} \
      --tester-type destination --port 50052
    """)
    processes.append(run(cmd, background=True))
    sleep(6)

    yield

    # Terminate gRPC server.
    server.stop(grace=3.0)

    # Terminate processes again.
    for proc in processes:
        proc.terminate()
        proc.wait(3)


# The record that is inserted into the database.
RECORD_REFERENCE = dict(  # noqa: C408
    unspecified="FOO",
    boolean=True,
    short=42,
    int=42,
    long=42,
    float=42.42,
    double=42.42,
    naive_date=86400000,
    naive_datetime=86400000,
    utc_datetime=86400000,
    decimal=42.42,
    binary="\\0x00\\0x01",
    string="Hotzenplotz",
    json={"count": 42, "foo": "bar"},
    xml="XML",
    naive_time=86400000,
    __fivetran_synced=mock.ANY,
    __fivetran_id="zyx-987-abc",
    __fivetran_deleted=None,
)


@pytest.mark.parametrize("services", ["./tests/data/fivetran_canonical"], indirect=True)
def test_integration_fivetran(capfd, services, engine):
    """
    Verify the Fivetran destination tester runs to completion with Fivetran test data.
    """

    # Read out stdout and stderr.
    out, err = capfd.readouterr()

    # "Truncate" is the last software test invoked by the Fivetran destination tester.
    # If the test case receives corresponding log output, it is considered to be complete.
    assert "Create Table succeeded: transaction" in err
    assert "Alter Table succeeded: transaction" in err
    assert "WriteBatch succeeded: transaction" in err
    assert "Truncate succeeded: transaction" in err

    assert "Create Table succeeded: campaign" in err
    assert "WriteBatch succeeded: campaign" in err
    assert "Truncate succeeded: campaign" in err
    assert "Hard Truncate succeeded: campaign" in err


@pytest.mark.parametrize("services", ["./tests/data/cratedb_canonical"], indirect=True)
def test_integration_cratedb(capfd, services, engine):
    """
    Verify the Fivetran destination tester runs to completion with CrateDB test data.
    """
    metadata = sa.MetaData()

    table_current = sa.Table(  # noqa: F841
        "all_types",
        metadata,
        schema="tester",
        quote_schema=True,
        autoload_with=engine,
    )

    table_reference = sa.Table(
        "all_types",
        metadata,
        sa.Column("unspecified", sa.String),
        sa.Column("bool", sa.Boolean),
        sa.Column("short", sa.SmallInteger),
        sa.Column("int", sa.Integer),
        sa.Column("long", sa.BigInteger),
        sa.Column("float", sa.Float),
        sa.Column("double", sa.Float),
        # FIXME: Investigate why `UserDefinedType` is used here.
        sa.Column("naive_date", UserDefinedType),
        sa.Column("naive_datetime", UserDefinedType),
        sa.Column("utc_datetime", UserDefinedType),
        sa.Column("decimal", sa.DECIMAL),
        sa.Column("binary", sa.Text),
        sa.Column("string", sa.String),
        sa.Column("json", ObjectType),
        sa.Column("xml", sa.String),
        sa.Column("naive_time", UserDefinedType),
        sa.Column("__fivetran_synced", UserDefinedType),
        sa.Column("__fivetran_id", sa.String),
        sa.Column("__fivetran_deleted", sa.Boolean),
        schema="tester_reference",
        quote_schema=True,
    )
    table_reference.schema = "tester"

    # Compare table schema.
    # FIXME: Comparison does not work like this, yet.
    #        Use Alembic's `compare()` primitive?
    # assert table_current == table_reference  # noqa: ERA001

    # Compare table content.
    with engine.connect() as connection:
        records = connection.execute(sa.text("SELECT * FROM tester.all_types")).mappings().one()
        assert records == RECORD_REFERENCE

    # Read out stdout and stderr.
    out, err = capfd.readouterr()

    # If the test case receives corresponding log output, it is considered to be complete.
    assert "Create Table succeeded: all_types" in err
    assert "WriteBatch succeeded: all_types" in err
