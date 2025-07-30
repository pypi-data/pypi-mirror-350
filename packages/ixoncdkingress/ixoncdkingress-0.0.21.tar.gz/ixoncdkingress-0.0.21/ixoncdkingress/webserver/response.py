"""Cloud Function response module."""
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

from ixoncdkingress.types import ContentType, ResponseCode

if TYPE_CHECKING:
    from _typeshed.wsgi import StartResponse

class Response:
    """
    Represents an HTTP response, containing headers and a body
    """
    body: bytes | None
    content_type: ContentType | None
    cookie: dict[str, str]
    headers: list[tuple[str, str]]
    start_response: 'StartResponse'
    status_code: ResponseCode

    def __init__(self, start_response: 'StartResponse') -> None:
        self.body = None
        self.content_type = None
        self.cookie = {}
        self.headers = []
        self.start_response = start_response
        self.status_code = ResponseCode.OK

    def __call__(self, *args: Any, **kwargs: Any) -> Iterable[bytes]:
        del args
        del kwargs

        headers = [*self.headers, *[('Set-Cookie', f'{k}={v}') for (k,v) in self.cookie.items()]]

        if self.content_type:
            headers.insert(0, ('Content-Type', f'{self.content_type.value}; charset=utf-8'))

        self.start_response(self.status_code.status_line(), headers)

        if self.body:
            return [self.body]

        return []

    def set_body(self, body: bytes) -> None:
        """
        Sets the body of the response
        """
        self.body = body
