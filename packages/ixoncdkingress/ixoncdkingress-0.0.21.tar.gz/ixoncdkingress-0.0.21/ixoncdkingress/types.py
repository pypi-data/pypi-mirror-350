"""
Module containing type aliases and enums
"""
import enum

FunctionLocation = tuple[str, str]
"""
Location of the function. First element specifies the Python module path, second element the
Python function name.
"""

FunctionArguments = dict[str, str]
"""Arguments to the function."""

class ContentType(enum.Enum):
    """
    HTTP content types which are used in the Content-Type headers
    """
    FORM = 'application/x-www-form-urlencoded'
    HTML = 'text/html'
    JSON = 'application/json'

class RequestMethod(enum.Enum):
    """
    Enum with valid HTTP methods
    """
    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
    PUT = 'PUT'
    OPTIONS = 'OPTIONS'

class ResponseCode(enum.Enum):
    """
    HTTP response codes to return
    """
    OK = 200
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    METHOD_NOT_ALLOWED = 405
    INTERNAL_ERROR = 500
    NOT_AVAILABLE = 503

    def status_line(self) -> str:
        """Produces a HTTP status line: <status-code> <message>"""
        return f"{self.value} {self.name.replace('_', ' ')}"
