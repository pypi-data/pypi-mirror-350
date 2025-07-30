"""
Contains the configuration for the ixoncdkingress webserver
"""
import enum
import json
import os
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from logging import Formatter, Logger, StreamHandler, getLogger
from typing import Any, Final

from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from load_environ_typed import LoaderMap, load
from load_environ_typed.loaders import load_utf8_file_from_path

try:
    from yaml import safe_load as yaml_safe_load
except ImportError:  # pragma: no cover
    yaml_safe_load = None  # type: ignore[assignment]

_LEGACY_CONTEXT_CONFIG_PATH: Final = "./context_config.json"
"""
Path to the (legacy) context config
"""

_JSON_CONTEXT_VALUES_PATH: Final = "./context_values.json"
"""
Path to a JSON file which can be used to load configuration values from.
"""

_YAML_CONTEXT_VALUES_PATH: Final = "./context_values.yaml"
"""
Path to a JSON file which can be used to load configuration values from.
"""

class InvalidConfigException(Exception):
    """
    Exception for invalid values in the config
    """

class WsgiProvider(enum.Enum):
    """
    Provider to use to turn a WSGI application into a (HTTP) server
    """
    WSGIREF = 'wsgiref'
    BJOERN = 'bjoern'
    WAITRESS = 'waitress'
    GUNICORN = 'gunicorn'
    CHERRYPY = 'cherrypy'
    MEINHELD = 'meinheld'

@dataclass
class Config:
    """
    Configuration for the webserver
    """
    production_mode: bool

    document_db_port: int

    http_server_bind: str
    http_server_port: int
    wsgi_provider: WsgiProvider

    logger_log_level: str
    logger_format: str

    cbc_path: str
    api_client_base_url: str

    cbc_signature_public_keys: list[str]

    _logger: Logger | None = None
    _signature_public_keys: list[ed25519.Ed25519PublicKey] | None = None

    @classmethod
    def from_environ(cls, environ: Mapping[str, str]) -> 'Config':
        """
        Deprecated, use get_config() instead.

        Parses an environment dictionary and generates a config based on it
        """
        return get_config(environ)

    def get_logger(self) -> Logger:
        """
        Returns a logger
        """
        if self._logger is None:
            logger = getLogger('ixoncdkingress')
            logger.setLevel(self.logger_log_level)

            handler = StreamHandler(sys.stdout)
            handler.setFormatter(Formatter(self.logger_format))
            logger.addHandler(handler)

            self._logger = logger

        return self._logger

    def get_signature_public_keys(self) -> list[ed25519.Ed25519PublicKey]:
        """
        Returns a cached instance of signature public keys
        """
        if self._signature_public_keys is None:
            keys: list[ed25519.Ed25519PublicKey] = []

            for index, pem in enumerate(self.cbc_signature_public_keys):
                key = load_pem_public_key(pem.encode('ASCII'), None)
                assert isinstance(key, ed25519.Ed25519PublicKey), \
                    f'signature_public_key {index + 1} is not a valid Ed25519 private key'
                keys.append(key)

            self._signature_public_keys = keys
        return self._signature_public_keys

def load_str_file(
        file_path: str | None, default: str
    ) -> str:
    """
    Loads a string from a file, returns default if no path is given
    """
    if not file_path:
        return default

    try:
        with open(file_path, encoding='utf-8') as file:
            string = file.read().rstrip()
            if not string:
                return default
        return string
    except OSError:
        return default

def load_json_file(
        file_path: str,
    ) -> dict[str, Any]:
    """
    Loads a Dict from a JSON file.
    """
    with open(file_path, encoding='utf-8') as file:
        result = json.load(file)

    if not isinstance(result, dict):
        raise ValueError('File must contain a dictionary')

    return result

def _load_yaml_file(
        file_path: str,
    ) -> dict[str, Any]:
    """
    Loads a Dict from a yaml file.
    """
    assert yaml_safe_load is not None, "PyYAML is not installed"

    with open(file_path, encoding='utf-8') as file:
        result = yaml_safe_load(file)

    if not isinstance(result, dict):
        raise ValueError('File must contain a dictionary')

    return result


def load_context_values(config: Config) -> dict[str, Any]:
    """
    Load context values from the config file(s).

    First try the YAML file, if it doesn't exist, then try to load the context values from the
    JSON file.
    If both YAML and JSON files don't exist, it will try to use the legacy context config JSON file
    and uses the values form the 'values' field, whereafter it also writes the values to the
    JSON file.
    """
    logger = config.get_logger()

    if os.path.exists(_YAML_CONTEXT_VALUES_PATH):
        if yaml_safe_load is None:
            raise ImportError(
                "Please install PyYAML to use context values from %s",
                _YAML_CONTEXT_VALUES_PATH,
            )
        logger.info("Loading context values from %s", _YAML_CONTEXT_VALUES_PATH)
        return _load_yaml_file(_YAML_CONTEXT_VALUES_PATH)

    if os.path.exists(_JSON_CONTEXT_VALUES_PATH):
        logger.info("Loading context values from %s", _JSON_CONTEXT_VALUES_PATH)
        logger.warning(
            "The file %s will be deprecated, please use %s instead. "
            "YAML is more readable and supports comments which can help during "
            "the configuration in the IXON Cloud",
            _JSON_CONTEXT_VALUES_PATH, _YAML_CONTEXT_VALUES_PATH
        )
        if os.path.exists(_LEGACY_CONTEXT_CONFIG_PATH):
            logger.info(
                "The file %s is unused and can be safely removed",
                _LEGACY_CONTEXT_CONFIG_PATH,
            )

        return load_json_file(_JSON_CONTEXT_VALUES_PATH)

    if os.path.exists(_LEGACY_CONTEXT_CONFIG_PATH):
        logger.info("Loading context config from %s", _LEGACY_CONTEXT_CONFIG_PATH)

        context_config = load_json_file(_LEGACY_CONTEXT_CONFIG_PATH)
        context_values = context_config.get('values')

        if isinstance(context_values, dict):
            logger.warning("The file %s is deprecated", _LEGACY_CONTEXT_CONFIG_PATH)
            logger.warning(
                "Contents of 'values' field from %s copied to %s.",
                _LEGACY_CONTEXT_CONFIG_PATH,
                _JSON_CONTEXT_VALUES_PATH,
            )
            logger.warning(
                "The file %s will no longer be used and can be safely removed.",
                _LEGACY_CONTEXT_CONFIG_PATH
            )
            with open(_JSON_CONTEXT_VALUES_PATH, 'w') as f:
                json.dump(context_values, f)

            return context_values

    return {}

def load_comma_separated_strings(raw: str) -> list[str]:
    return raw.split(',') if raw != '' else []

CONFIG_DEFAULTS = {
    'API_CLIENT_BASE_URL': 'https://api.ayayot.com/',
    'CBC_PATH': '/user_scripts',
    'CBC_SIGNATURE_PUBLIC_KEYS': '',
    'DOCUMENT_DB_PORT': '27017',
    'HTTP_SERVER_BIND': '127.0.0.1',
    'HTTP_SERVER_PORT': '8020',
    'LOGGER_FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'LOGGER_LOG_LEVEL': 'INFO',
    'PRODUCTION_MODE': 'False',
    'WSGI_PROVIDER': 'wsgiref',
}

CONFIG_LOADERS: LoaderMap = {
    'cbc_signature_public_keys': load_comma_separated_strings,
    'version': load_utf8_file_from_path,
    'wsgi_provider': WsgiProvider,
}

def get_config(environ: Mapping[str, str] | None = None) -> Config:
    return load(Config, environ=environ, defaults=CONFIG_DEFAULTS, loaders=CONFIG_LOADERS)
