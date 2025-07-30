import logging
import sys


class Logger:
    """
    A logger utility class to provide structured and formatted logging for applications.

    This class allows logging messages at various severity levels (debug, info, warning,
    error). Log messages are formatted to include timestamp, logger name, log
    level, filename, line number, and the message content.

    The logger outputs to the console (stdout) using a formatted stream handler.
    If a logger already exists for the specified name, any existing handlers are cleared
    to avoid duplicate logging.

    Parameters
    ----------
    module : str, optional
        The name of the module or component using the logger. If provided, it is included
        in the logger name.

    Attributes
    ----------
    logger : logging.Logger
        The internal logger instance used to handle logging operations.

    Example
    -------
    Creating and using a logger instance:

    >>> log = Logger(module="my_module")
    >>> log.info("This is an info message.")
    >>> log.error("This is an error message.")
    """

    def __init__(self, module=None, level=logging.DEBUG):
        formatter = logging.Formatter(
            "%(asctime)s — %(name)s — %(levelname)s — %(filename)s — %(funcName)s — %(lineno)s — %(message)s"
        )
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        logger_name = None

        if module:
            logger_name = module

        self.logger = logging.getLogger(logger_name)

        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        self.logger.addHandler(console_handler)
        self.logger.setLevel(level)
        self.logger.propagate = False

    def debug(self, message, stacklevel=2, truncation=None):
        if truncation is not None and len(str(message)) > truncation:
            message = message[:truncation] + "..."
        self.logger.debug(message, stacklevel=stacklevel)

    def info(self, message, stacklevel=2, truncation=None):
        if truncation is not None and len(str(message)) > truncation:
            message = message[:truncation] + "..."
        self.logger.info(message, stacklevel=stacklevel)

    def warning(self, message, stacklevel=2, truncation=None):
        if truncation is not None and len(str(message)) > truncation:
            message = message[:truncation] + "..."
        self.logger.warning(message, stacklevel=stacklevel)

    def error(self, message, stacklevel=2, truncation=None):
        if truncation is not None and len(str(message)) > truncation:
            message = message[:truncation] + "..."
        self.logger.error(message, stacklevel=stacklevel)
