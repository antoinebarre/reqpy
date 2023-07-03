#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python dual-logging setup (console and log file),
supporting different log levels and colorized output.

Created by Fonic <https://github.com/fonic>
Date: 04/05/20 - 02/07/23

Based on:
https://stackoverflow.com/a/13733863/1976617
https://uran198.github.io/en/python/2016/07/12/colorful-python-logging.html
https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
"""

import os
import sys
import logging

from typing import Any, Optional, Union


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

    def format(self, record: logging.LogRecord, *args: Any, **kwargs: Any) -> str:
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


def set_up_logging(
    console_log_output: str,
    console_log_level: str,
    console_log_color: bool,
    logfile_file: str,
    logfile_log_level: str,
    logfile_log_color: bool,
    log_line_template: str
) -> bool:
    """
    Set up logging for console and log file.

    Args:
        console_log_output (str): The console log output ("stdout" or "stderr").
        console_log_level (str): The console log level.
        console_log_color (bool): Whether to use color in console logs.
        logfile_file (str): The log file name.
        logfile_log_level (str): The log file log level.
        logfile_log_color (bool): Whether to use color in log file logs.
        log_line_template (str): The log line template.

    Returns:
        bool: True if logging is set up successfully, False otherwise.
    """
    # Create logger
    logger = logging.getLogger()

    # Set global log level to 'debug' (required for handler levels to work)
    logger.setLevel(logging.DEBUG)

    # Create console handler
    console_log_output = console_log_output.lower()
    if console_log_output == "stdout":
        console_log_output = sys.stdout
    elif console_log_output == "stderr":
        console_log_output = sys.stderr
    else:
        print(f"Failed to set console output: invalid output: '{console_log_output}'")
        return False
    console_handler = logging.StreamHandler(console_log_output)

    # Set console log level
    try:
        console_handler.setLevel(console_log_level.upper())  # only accepts uppercase level names
    except:
        print(f"Failed to set console log level: invalid level: '{console_log_level}'")
        return False

    # Create and set formatter, add console handler to logger
    console_formatter = LogFormatter(fmt=log_line_template, color=console_log_color)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Create log file handler
    try:
        logfile_handler = logging.FileHandler(logfile_file)
    except Exception as exception:
        print(f"Failed to set up log file: {str(exception)}")
        return False

    # Set log file log level
    try:
        logfile_handler.setLevel(logfile_log_level.upper())  # only accepts uppercase level names
    except:
        print(f"Failed to set log file log level: invalid level: '{logfile_log_level}'")
        return False

    # Create and set formatter, add log file handler to logger
    logfile_formatter = LogFormatter(fmt=log_line_template, color=logfile_log_color)
    logfile_handler.setFormatter(logfile_formatter)
    logger.addHandler(logfile_handler)

    # Success
    return True


def main() -> int:
    """
    Main function.

    Returns:
        int: The exit code.
    """
    # Set up logging
    script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if not set_up_logging(
        console_log_output="stdout",
        console_log_level="warning",
        console_log_color=True,
        logfile_file=script_name + ".log",
        logfile_log_level="debug",
        logfile_log_color=False,
        log_line_template="%(color_on)s[%(created)d] [%(threadName)s] [%(levelname)-8s] %(message)s%(color_off)s"
    ):
        print("Failed to set up logging, aborting.")
        return 1

    # Log some messages
    logging.debug("Debug message")
    logging.info("Info message")
    logging.warning("Warning message")
    logging.error("Error message")
    logging.critical("Critical message")

    return 0


if __name__ == "__main__":
    sys.exit(main())
