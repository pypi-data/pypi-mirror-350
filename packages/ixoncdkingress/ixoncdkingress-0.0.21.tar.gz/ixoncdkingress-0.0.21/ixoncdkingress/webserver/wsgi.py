"""
WGSI implementation for ixoncdkingress
"""
import functools
import signal
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

from ixoncdkingress.types import RequestMethod, ResponseCode
from ixoncdkingress.webserver.config import Config, WsgiProvider
from ixoncdkingress.webserver.request import Request
from ixoncdkingress.webserver.response import Response
from ixoncdkingress.webserver.servlet import Servlet
from ixoncdkingress.webserver.utils import setup_mongo_container, shutdown_mongo_container

if TYPE_CHECKING:
    from _typeshed.wsgi import StartResponse, WSGIApplication, WSGIEnvironment

def restapi_wsgi(
        config: Config,
        servlet: Servlet,
        environ: 'WSGIEnvironment',
        start_response: 'StartResponse',
    ) -> Iterable[bytes]:
    """
    Main application to give to a WSGI-capable (HTTP) server
    """
    request = Request(config, environ)
    response = Response(start_response)

    try:
        do_servlet_method(servlet, request, response)
    except NotImplementedError:
        return start_error_response(start_response)

    return response()

def do_servlet_method(
        servlet: Servlet,
        request: Request,
        response: Response
    ) -> None:
    """
    Calls the Servlet method specified by the `request.request_method`
    """
    if RequestMethod.OPTIONS == request.request_method:
        servlet.do_options(request, response)
    elif RequestMethod.GET == request.request_method and not servlet.config.production_mode:
        # Get requests are only allowed in development (non production mode)
        servlet.do_get(request, response)
    elif RequestMethod.POST == request.request_method:
        servlet.do_post(request, response)
    else:
        raise NotImplementedError

def start_error_response(
        start_response: 'StartResponse',
    ) -> Iterable[bytes]:
    """
    Creates a new Response producing an error response
    """
    error_response = Response(start_response)
    error_response.status_code = ResponseCode.METHOD_NOT_ALLOWED
    return error_response()

def run_server(config: Config, servlet: Servlet) -> None:
    """
    Runs the WGSI server with the given provider
    """
    handler = PROVIDER_MAP[config.wsgi_provider]

    signal.signal(signal.SIGTERM, raise_ki_on_signal)

    handler(config, wsgi_application=functools.partial(restapi_wsgi, config, servlet))

def raise_ki_on_signal(signum: Any, frame: Any) -> None:
    """
    Raises a KeyboardInterrupt

    For use in signal handling
    """
    del signum
    del frame

    raise KeyboardInterrupt

def run_server_wsgiref(config: Config, wsgi_application: 'WSGIApplication') -> None:
    """
    Runs the server using the wsgi reference application
    """
    logger = config.get_logger()

    import wsgiref.simple_server

    dev_container = setup_mongo_container(config)

    server = wsgiref.simple_server.make_server(
        config.http_server_bind, config.http_server_port,
        wsgi_application,
    )

    with server as httpd:
        logger.info(
            'wsgiref listening on http://%s:%s/',
            config.http_server_bind,
            config.http_server_port
        )
        logger.info(
            'CBC_PATH: %s', config.cbc_path
        )
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info('Caught keyboard interrupt')
            if dev_container:
                shutdown_mongo_container(config, dev_container)
            httpd.shutdown()


PROVIDER_MAP = {
    WsgiProvider.WSGIREF: run_server_wsgiref,
}
