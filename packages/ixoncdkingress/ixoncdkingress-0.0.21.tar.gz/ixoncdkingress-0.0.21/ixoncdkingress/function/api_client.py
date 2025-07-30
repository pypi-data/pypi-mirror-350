"""
Contains code dealing with API clients
"""
import json
from collections.abc import MutableMapping
from typing import Any

import requests

Query = MutableMapping[str, None | str | list[str]]

ClientRequest = dict[str, Any] | list[dict[str, Any]] | bytes

ServerResponse = dict[str, Any]

class ApiClient:
    """
    class for a API client
    """

    _base_url: str
    """
    The base URL (entry point) of the API server
    """

    _default_headers: dict[str, str]
    """
    The headers to send along with every request
    """

    _session: requests.Session
    """
    Requests session to run requests with
    """

    _discovery: dict[str, str] | None
    """
    Discovery dictionary
    """

    def __init__(
        self,
        base_url: str,
        api_application: str | None = None,
        api_company: str | None = None,
        authorization: str | None = None,
    ) -> None:
        self._base_url = base_url

        self._default_headers = {
            'Api-Version': '2',
        }

        if api_application:
            self._default_headers['Api-Application'] = api_application
        if api_company:
            self._default_headers['Api-Company'] = api_company
        if authorization:
            self._default_headers['Authorization'] = authorization

        self._session = requests.session()

        self._discovery = None

    def _check_discovery(self, verify: bool = True) -> None:
        """
        Checks whether discovery has been run, and, if not, runs it.

        Set verify on True when the certificate shouldn't be checked, which is the case when
        the ApiClient has to talk to the envdev ixapi-server.

        We don't expire the discovery as a new ApiClient instance is
        created for every Cloud Function call.
        """
        if self._discovery is not None:
            return

        discovery_headers =  {'Api-Version': self._default_headers['Api-Version']}
        response = self._session.get(self._base_url, headers=discovery_headers, verify=verify)
        assert response.ok, 'Api discovery failed'
        data = response.json()
        assert 'Discovery' == data['type']
        self._discovery = {
            discovery['rel']: discovery['href']
            for discovery in data['data']
        }

    def set_custom_api_application(self, api_application: str) -> None:
        """
        Modifies the Api-Application header used for API server requests.
        """
        self._default_headers['Api-Application'] = api_application

    def get(
            self,
            url_name: str,
            url_args: dict[str, str] | None = None,
            query: Query | None = None,
            headers: dict[str, str] | None = None,
            **kwargs: Any
        ) -> ServerResponse:
        """
        Performs a GET request on the API server, on the URL with the given
        name

        The URL names are found in the discovery
        """
        return self._request(
            'GET', url_name, url_args=url_args, query=query, headers=headers, **kwargs
        )

    def patch(
            self,
            url_name: str,
            data: ClientRequest,
            url_args: dict[str, str] | None = None,
            query: Query | None = None,
            headers: dict[str, str] | None = None,
            **kwargs: Any
        ) -> ServerResponse:
        """
        Performs a PATCH request on the API server, on the URL with the given
        name

        The URL names are found in the discovery
        """
        return self._request(
            'PATCH', url_name, url_args=url_args, query=query, data=data, headers=headers, **kwargs
        )

    def post(
            self,
            url_name: str,
            data: ClientRequest,
            url_args: dict[str, str] | None = None,
            query: Query | None = None,
            headers: dict[str, str] | None = None,
            **kwargs: Any
        ) -> ServerResponse:
        """
        Performs a POST request on the API server, on the URL with the given
        name

        The URL names are found in the discovery
        """
        return self._request(
            'POST', url_name, url_args=url_args, query=query, data=data, headers=headers, **kwargs
        )

    def options(
            self,
            url_name: str,
            url_args: dict[str, str] | None = None,
            headers: dict[str, str] | None = None,
            **kwargs: Any
        ) -> ServerResponse:
        """
        Performs an OPTIONS request on the API server, on the URL with the given
        name

        The URL names are found in the discovery

        When using a browser, these are done automatically. When not using a browser,
        these are not required
        """
        return self._request(
            'OPTIONS', url_name, url_args=url_args, headers=headers, **kwargs
        )

    def put(
            self,
            url_name: str,
            url_args: dict[str, str] | None = None,
            data: ClientRequest | None = None,
            headers: dict[str, str] | None = None,
            **kwargs: Any
        ) -> dict[str, Any]:
        """
        Performs a PUT request on the API server, on the URL with the given
        name

        The URL names are found in the discovery
        """
        return self._request(
            'PUT', url_name, url_args=url_args, data=data, headers=headers, **kwargs
        )

    def delete(
            self,
            url_name: str,
            url_args: dict[str, str] | None = None,
            data: ClientRequest | None = None,
            query: Query | None = None,
            headers: dict[str, str] | None = None,
            **kwargs: Any
        ) -> ServerResponse:
        """
        Performs a DELETE request on the API server, on the URL with the given
        name

        The URL names are found in the discovery
        """
        return self._request(
            'DELETE', url_name, url_args=url_args, query=query, data=data, headers=headers,
            **kwargs
        )

    def _request(
            self,
            method: str,
            url_name: str,
            url_args: dict[str, str] | None = None,
            headers: dict[str, str] | None = None,
            query: Query | None = None,
            data: ClientRequest | None = None,
            **kwargs: Any,
        ) -> ServerResponse:
        """
        Sends a request to the API server
        """
        if url_args is None:
            url_args = {}

        url = self._get_url(url_name, url_args, kwargs.get('verify', True))

        if headers is None:
            headers = {}

        data_json: bytes | None
        if data is None or isinstance(data, bytes):
            data_json = data
        else:
            data_json = json.dumps(data).encode('UTF-8')

        response = self._session.request(
            method, url,
            params=query,
            headers={
                **self._default_headers,
                **headers,
            },
            data=data_json,
            **kwargs,
        )
        try:
            return response.json() # type: ignore[no-any-return]
        except json.decoder.JSONDecodeError:
            return {
                'type': 'Error',
                'data': [
                    {
                        'message': response.text,
                    }
                ],
                'status': 'error'
            }

    def _get_url(self, url_name: str, url_args: dict[str, str], verify: bool = True) -> str:
        """
        Returns an URL by name from the discovery and apply the URL arguments
        """
        self._check_discovery(verify=verify)
        assert self._discovery is not None # type hint

        return self._discovery[url_name].format(**url_args)

    def __repr__(self) -> str:
        return (
            '<ApiClient'
            f' base_url={self._base_url},'
            f' default_headers={self._default_headers},'
            '>'
        )
