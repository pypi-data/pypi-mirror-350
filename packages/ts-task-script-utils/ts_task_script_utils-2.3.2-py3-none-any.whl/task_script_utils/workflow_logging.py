import logging

TS_LOG_LEVEL_MAP = {
    "DEBUG": "debug",
    "INFO": "info",
    "WARNING": "warn",
    "ERROR": "error",
    "CRITICAL": "crit",
}


def map_ts_log_level(log_level_name: str) -> str:
    """Convert Python's logging levels to TetraScience log levels

    Arguments:
        logging_level_name (str) - Python's logging level name ("DEBUG",
            "WARNING", etc.)

    Returns:
        ts_log_level_name (str) - TetraScience log level string
    """
    if log_level_name not in TS_LOG_LEVEL_MAP:
        raise KeyError(
            f"Log level `{log_level_name}` has no corresponding TetraScience level name"
        )
    return TS_LOG_LEVEL_MAP[log_level_name]


class TSLogFormatter(logging.Formatter):
    """Log formatter to convert python logs into the TetraScience format"""

    def __init__(self):
        super().__init__()

    def format(self, record):
        record.message = record.getMessage()
        ts_log_record = {
            "level": map_ts_log_level(record.levelname),
            "message": record.message,
            "funcName": record.module + "." + record.funcName,
        }
        return ts_log_record


class TSLogHandler(logging.StreamHandler):
    """A log handler to redirect Python's logs to an external logger function"""

    def __init__(self, external_logger: object) -> None:
        """Initialize a log handler with a pointer to the external logging
        function, and a formatter to convert log into a dictionary expected
        by the workflow object.

        Arguments:
            external_logger (object) - A TetraScience workflow logger object,
                external_logger.log(log_record)
        """
        super().__init__()

        self.external_logger = external_logger
        self.setFormatter(TSLogFormatter())

    def handle(self, record: logging.LogRecord) -> None:
        """Redirect log output to the external logger object's log function

        A custom formatter structures the log into the form required by the
        workflow logger.log function

        Arguments:
            record {logging.LogRecord} - Log record including message and level
        """
        ts_record = self.format(record)
        self.external_logger.log(ts_record)


def setup_ts_log_handler(
    external_logger: object, logger_scope: str = None
) -> logging.Logger:
    """Set up a handler to send Python logs to the TetraScience workflow logger

    After setting up this log handler, any logger created within the same
    logging hierarchy will have its logs sent to the external logger (see
    logging.getLogger docs for more on logging heirarchy).

    Arguments:
        external_logger (object) - The external logging object to pass logs to.
            external_logger.log(record) will be called with a record formatted
            as a TetraScience log record.
        logger_scope (str) - the name passed to logging.getLogger(logger_scope)
            which defines the heirarchy of logs handled by the external logger.
    """
    logger = logging.getLogger(logger_scope)
    logger.setLevel(logging.INFO)
    logger.addHandler(TSLogHandler(external_logger))
