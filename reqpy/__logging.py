"""logging tools for reqpy module"""


from pathlib import Path
import sys
import logging
from enum import Enum
from typing import Any, Callable
from rich.console import Console
from rich.theme import Theme
import functools

# logging
logger = logging.getLogger(__name__)


# Define console Theme
custom_theme = Theme({
    "title": "bold white on dodger_blue3",
    "apps": "bold blue",
    "activity": "purple italic",
    "info": "cyan",
    "ok": "green",
    "ko": "red"
})

console = Console(theme=custom_theme)

FORMAT_THEME = {
    "TITLE": {
        "style": "title",
        "align": "center",
        "before": "",
        "after": "",
    },
    "APPS": {
        "style": "apps",
        "align": "left",
        "before": "\n>>> ",
        "after": "\n",
    },
    "ACTIVITY": {
        "style": "activity",
        "align": "left",
        "before": " - ",
        "after": "...",
    },
    "INFO": {
        "style": "info",
        "align": "left",
        "before": "",
        "after": "\n",
    },
    "OK": {
        "style": "ok",
        "align": "left",
        "before": "",
        "after": "\n",
    },
    "KO": {
        "style": "ko",
        "align": "left",
        "before": "",
        "after": "\n",
    },
}


def printConsole(
        *,
        message: str,
        type: str = "INFO",
        show_console: bool
        ) -> None:

    # exist if no console
    if not show_console:
        return None

    if type in FORMAT_THEME:

        # modify message
        message = (FORMAT_THEME[type]["before"] +
                   message +
                   FORMAT_THEME[type]["after"])
        # console output
        console.print(
            message,
            style=FORMAT_THEME[type]["style"],
            justify=FORMAT_THEME[type]["align"])  # type: ignore
        # logging output
        logger.log(
            level=logging.DEBUG,
            msg="CONSOLE OUTPUT : " + message)
    else:
        raise ValueError(
            (f"{type} is not in the list of console theme (i.e.):"
             f"{str(FORMAT_THEME.keys())}")
            )


class LogLevel(str, Enum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
                '%r is not a valid %s.  Valid types: %s' % (
                    value,
                    cls.__name__,
                    ', '.join([repr(m.value) for m in cls]),
                    ))

    def __int__(self) -> int:

        # see https://docs.python.org/3/library/logging.html#logging-levels
        if self.value == "CRITICAL":
            return 50
        elif self.value == "ERROR":
            return 40
        elif self.value == "WARNING":
            return 30
        elif self.value == "INFO":
            return 20
        elif self.value == "DEBUG":
            return 10
        else:
            return 0


class LogFormatter(logging.Formatter):
    """
    Logging formatter supporting colorized output.
    """

    COLOR_CODES = {
        logging.CRITICAL: "\033[1;35m",  # bright/bold magenta
        logging.ERROR: "\033[1;31m",  # bright/bold red
        logging.WARNING: "\033[1;33m",  # bright/bold yellow
        logging.INFO: "\033[0;37m",  # white / light gray
        logging.DEBUG: "\033[1;30m"  # bright/bold black / dark gray
    }

    RESET_CODE = "\033[0m"

    def __init__(self, color: bool, *args: Any, **kwargs: Any) -> None:
        super(LogFormatter, self).__init__(*args, **kwargs)
        self.color = color

    def format(
            self,
            record: logging.LogRecord,
            *args: Any, **kwargs: Any) -> str:
        """
        Format the log record.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log record.
        """
        if self.color and record.levelno in self.COLOR_CODES:
            record.color_on = self.COLOR_CODES[record.levelno]
            record.color_off = self.RESET_CODE
        else:
            record.color_on = ""
            record.color_off = ""
        return super(LogFormatter, self).format(record, *args, **kwargs)


def setup_logging(
    *,
    console_log_level: LogLevel = LogLevel.WARNING,
    console_log_format: str = (
        "%(color_on)s[%(funcName)-s][%(levelname)-8s] %(message)s%(color_off)s"
    ),
    logfile_log_level: LogLevel = LogLevel.DEBUG,
    logfile_file: Path = Path("log_reqpy.log"),
    logfile_format: str = (
        '%(asctime)s %(filename)20s/%(funcName)20s'
        ' - %(levelname)8s:%(message)s%(color_off)s'
        )
) -> None:
    """
    Set up logging for console and log file.

    Args:
        console_log_level (LogLevel): The console log level.
          Default is LogLevel.INFO.
        console_log_format (str): The console log format.
        logfile_log_level (LogLevel): The log file log level.
          Default is LogLevel.DEBUG.
        logfile_file (Path): The log file path.
          Default is Path("log_reqpy.log").
        logfile_format (str): The log file format.

    Returns:
        None: There is no return value.

    """
    # Create logger
    logger = logging.getLogger()

    # Set global log level to 'debug' (required for handler levels to work)
    logger.setLevel(logging.DEBUG)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)

    # Set console log level
    console_handler.setLevel(LogLevel(console_log_level).value)

    # Create and set formatter, add console handler to logger
    console_formatter = LogFormatter(fmt=console_log_format, color=True)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Create log file handler
    logfile_handler = logging.FileHandler(logfile_file)

    # Set log file log level
    logfile_handler.setLevel(LogLevel(logfile_log_level).value)

    # Create and set formatter, add log file handler to logger
    logfile_formatter = LogFormatter(fmt=logfile_format, color=False)
    logfile_handler.setFormatter(logfile_formatter)
    logger.addHandler(logfile_handler)

    # Success
    return None


# logging wrapper
def with_logging(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.debug(f">>> Calling {func.__name__}")
        value = func(*args, **kwargs)
        logger.debug(f">>> Finished {func.__name__}")
        return value

    return wrapper
