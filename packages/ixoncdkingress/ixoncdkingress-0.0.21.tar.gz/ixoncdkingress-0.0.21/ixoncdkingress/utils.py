"""
Module containing utility functions
"""
import traceback

from ixoncdkingress.types import ResponseCode
from ixoncdkingress.webserver.response import Response


def handle_exception(exception: BaseException, response: Response) -> None:
    """
    Shows the error with traceback in the console and sets the response status code to 500.
    """
    traceback.print_exception(None, exception, exception.__traceback__)

    response.status_code = ResponseCode.INTERNAL_ERROR
