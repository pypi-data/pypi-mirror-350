import logging

import click

from cratedb_fivetran_destination.main import start_server
from cratedb_fivetran_destination.util import setup_logging

logger = logging.getLogger()


@click.command()
@click.version_option()
@click.pass_context
@click.option("--host", "-h", type=str, default="[::]", help="Host to listen on. Default: [::]")
@click.option("--port", "-p", type=int, default=50052, help="Port to listen on. Default: 50052")
@click.option(
    "--max-workers",
    "-w",
    type=int,
    default=1,
    help="The maximum number of threads that can be used. Default: 1",
)
def main(ctx: click.Context, host: str, port: int, max_workers: int) -> None:
    """
    Start Fivetran CrateDB Destination gRPC server.

    Options:

        --port: Port number to listen on. By default, listen on port 50052.

        --host: Host to listen on. By default, listen on both IPV4 (0.0.0.0) and IPV6 (::0).
    """
    setup_logging()
    server = start_server(host=host, port=port, max_workers=max_workers)
    logger.info(f"Fivetran CrateDB Destination gRPC server started on {host}:{port}")
    server.wait_for_termination()
    logger.info("Fivetran CrateDB Destination gRPC server terminated")


if __name__ == "__main__":  # pragma: nocover
    main()
