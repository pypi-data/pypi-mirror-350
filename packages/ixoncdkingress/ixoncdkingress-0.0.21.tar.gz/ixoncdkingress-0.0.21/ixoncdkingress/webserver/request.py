"""Cloud Function request module."""
import json
from http.cookies import SimpleCookie
from typing import TYPE_CHECKING, Any
from urllib.parse import parse_qs

from ixoncdkingress.types import ContentType, RequestMethod
from ixoncdkingress.webserver.config import Config

if TYPE_CHECKING:
    from _typeshed.wsgi import WSGIEnvironment

class Request:
    """
    Represents an HTTP request, containing headers and optionally a body
    """
    body: dict[str, Any] | None
    config: Config
    content_type: ContentType | None
    authorization: str | None
    cookies: SimpleCookie | None
    request_body: bytes
    request_method: RequestMethod

    def __init__(self, config: Config, environ: 'WSGIEnvironment') -> None:
        self.config = config
        self.request_method = RequestMethod(environ['REQUEST_METHOD'])
        self.body = None

        if cookies_env := environ.get('HTTP_COOKIE'):
            self.cookies = SimpleCookie(cookies_env)
        else:
            self.cookies = None

        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            self.request_body = environ['wsgi.input'].read(request_body_size)
        except ValueError:
            self.request_body = b''

        try:
            self.content_type = ContentType(environ['CONTENT_TYPE'])
        except (KeyError, ValueError):
            self.content_type = None

        try:
            self.authorization = environ['HTTP_AUTHORIZATION']
        except KeyError:
            self.authorization = None

    def parse_body(self) -> None:
        """
        Parses the request body according to the `content_type`.

        Must only be called once.
        """
        assert self.body is None

        if ContentType.FORM == self.content_type:
            self.body = parse_qs(self.request_body.decode('utf-8'))
        elif ContentType.JSON == self.content_type:
            self.body = json.loads(self.request_body)
        else:
            raise NotImplementedError
