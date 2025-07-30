"""
Context.
"""
import warnings
from inspect import _empty, signature
from typing import Any

from pymongo import MongoClient

from ixoncdkingress.function.api_client import ApiClient
from ixoncdkingress.function.document_db_client import DocumentDBClient, DocumentType
from ixoncdkingress.function.time_series_client import TimeSeriesClient


class FunctionResource:
    """
    Describes an IXAPI resource.
    """
    public_id: str
    name: str
    custom_properties: dict[str, Any]
    permissions: set[str] | None

    def __init__(
            self,
            public_id: str,
            name: str,
            custom_properties: dict[str, Any],
            permissions: set[str] | None
        ) -> None:
        self.public_id = public_id
        self.name = name
        self.custom_properties = custom_properties
        self.permissions = permissions

    def __repr__(self) -> str:
        return (
            '<FunctionResource'
            f' public_id={self.public_id},'
            f' name={self.name},'
            f' custom_properties={self.custom_properties!r},'
            f' permissions={self.permissions!r},'
            f'>'
        )

class FunctionContext:
    """
    The context for a Cloud Function.
    """
    config: dict[str, str]
    api_client: ApiClient
    user: FunctionResource | None
    company: FunctionResource | None
    asset: FunctionResource | None
    agent: FunctionResource | None
    template: FunctionResource | None

    _mongo_client: MongoClient[DocumentType] | None
    _ddb_collection_name: str

    @property
    def document_db_client(self) -> DocumentDBClient | None:
        """
        The client for accessing the default collection of the Document DB.

        This may be None when running the Cloud Function in development mode,
        and using the local debug form without specifying a company.
        """
        if not self._mongo_client or not self.company:
            return None

        return DocumentDBClient(
            self._mongo_client[self.company.public_id][self._ddb_collection_name]
        )

    @property
    def time_series_client(self) -> TimeSeriesClient | None:
        """
        The client for accessing the time series collection of the Cloud Function.

        WARNING: This function and client is experimental and may change in the future.

        This may be None when running the Cloud Function in development mode,
        and using the local debug form without specifying a company.
        """
        warnings.warn(
            "The TimeSeriesClient is experimental and may change in the future",
            category=FutureWarning,
        )

        if not self._mongo_client or not self.company:
            return None

        return TimeSeriesClient(
            self._mongo_client[self.company.public_id][f"{self._ddb_collection_name}_ts"]
        )

    @property
    def agent_or_asset(self) -> FunctionResource:
        """
        Return either an Agent or an Asset resource, depending on what's available. If both are
        available in the context, returns the Asset resource.
        """
        if self.asset:
            return self.asset

        assert self.agent
        return self.agent

    def __init__(
            self,
            config: dict[str, str],
            api_client: ApiClient,
            mongo_client: MongoClient[DocumentType] | None,
            user: FunctionResource | None,
            company: FunctionResource | None,
            asset: FunctionResource | None,
            agent: FunctionResource | None,
            template: FunctionResource | None,
            document_db_collection_name: str,
        ) -> None:

        self.config = config
        self.api_client = api_client
        self.user = user
        self.company = company
        self.asset = asset
        self.agent = agent
        self.template = template

        self._mongo_client = mongo_client
        self._ddb_collection_name = document_db_collection_name

    def __repr__(self) -> str:
        return (
            f'<FunctionContext'
            f' config={self.config!r},'
            f' api_client={self.api_client!r},'
            f' document_db_client={self.document_db_client!r},'
            f' user={self.user!r},'
            f' company={self.company!r},'
            f' asset={self.asset!r},'
            f' agent={self.agent!r},'
            f' template={self.template!r},'
            f'>'
        )

    @staticmethod
    def expose(function: Any) -> Any:
        """
        Decorator to mark a function as an exposed endpoint.
        """
        sig = signature(function, eval_str=True)

        if not sig.parameters:
            raise Exception('Function has no argument for FunctionContext')

        # If the first function argument has a type annotation it should be of FunctionContext
        context_param = sig.parameters[next(iter(sig.parameters))]
        if (context_param.annotation is not _empty
                and context_param.annotation is not FunctionContext):
            raise Exception('First function parameter should be of type FunctionContext')

        function.exposed = True

        return function
