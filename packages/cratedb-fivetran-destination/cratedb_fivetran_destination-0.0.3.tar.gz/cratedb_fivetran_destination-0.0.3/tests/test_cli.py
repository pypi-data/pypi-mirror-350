import pytest
from click.testing import CliRunner

from cratedb_fivetran_destination.cli import main


@pytest.fixture
def cli_runner() -> CliRunner:
    return CliRunner()


def test_cli_version(cli_runner, mocker):
    """
    CLI test: Invoke `cratedb-fivetran-destination --version`.
    """
    result = cli_runner.invoke(
        main,
        args="--version",
        catch_exceptions=False,
    )
    assert result.exit_code == 0


def test_cli_real_mocked(cli_runner, mocker):
    """
    CLI test: Invoke `cratedb-fivetran-destination`.
    """
    mocker.patch("cratedb_fivetran_destination.cli.start_server")
    result = cli_runner.invoke(
        main,
        args="",
        catch_exceptions=False,
    )
    assert result.exit_code == 0
