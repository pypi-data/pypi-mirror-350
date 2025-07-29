import json
import logging
import sys

LOG_INFO = "INFO"
LOG_WARNING = "WARNING"
LOG_SEVERE = "SEVERE"


def log_message(level, message):
    print(format_log_message(message=message, level=level))  # noqa: T201


def format_log_message(message: str, level="INFO", newline=False):
    suffix = newline and "\n" or ""
    return (
        json.dumps({"level": level, "message": message, "message-origin": "sdk_destination"})
        + suffix
    )


def setup_logging(level=logging.INFO, verbose: bool = False):
    if verbose:
        level = logging.DEBUG
    log_format = "%(asctime)-15s [%(name)-26s] %(levelname)-8s: %(message)s"
    logging.basicConfig(format=log_format, stream=sys.stderr, level=level, force=True)
