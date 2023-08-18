""" Collect all the exceptions used by reqpy"""

from click import ClickException


class RequirementException(ClickException):
    """Exception raised by the Requirement object"""
    pass


class ReqpyPathException(ClickException):
    """Exception raised by Path handling error"""
    pass


class ReqpyIOException(ClickException):
    """Exception raised by file IO errors"""
    pass


class ReqpyDBException(ClickException):
    """Exception raised during the handling of file as database"""
