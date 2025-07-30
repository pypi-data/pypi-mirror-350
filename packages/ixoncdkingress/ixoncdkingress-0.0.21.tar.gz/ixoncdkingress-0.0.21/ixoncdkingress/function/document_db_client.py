"""
Document DB client & related types
"""
import warnings
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any, TypeAlias

from pymongo.results import (
    DeleteResult,
    InsertManyResult,
    InsertOneResult,
    UpdateResult,
)

from ixoncdkingress.function._collection import Collection

DocumentType: TypeAlias = Mapping[str, Any]

class DocumentDBClient(Collection[DocumentType]): # pragma: no-cov
    """
    Client for a Document DB collection.
    """

    def insert_one(self, document: DocumentType) -> InsertOneResult:
        """
        Insert a single document into the store.
        """
        return self._collection.insert_one(document)

    def insert_many(self, documents: Iterable[DocumentType]) -> InsertManyResult:
        """
        Insert an iterable of documents into of store.
        """
        return self._collection.insert_many(documents)

    def update_one(self, filter_map: Mapping[str, Any], update: Mapping[str, Any]) -> UpdateResult:
        """
        Update a single document matching the filter.
        """
        return self._collection.update_one(filter_map, update)

    def update_many(self, filter_map: Mapping[str, Any], update: Mapping[str, Any]) -> UpdateResult:
        """
        Update one or more documents that match the filter.
        """
        return self._collection.update_many(filter_map, update)

    def delete_one(self, filter_map: Mapping[str, Any]) -> DeleteResult:
        """
        Delete a single document matching the filter.
        """
        return self._collection.delete_one(filter_map)

    def delete_many(self, filter_map: Mapping[str, Any]) -> DeleteResult:
        """
        Delete one or more documents matching the filter.
        """
        return self._collection.delete_many(filter_map)


@dataclass(frozen=True, init=False)
class DocumentDBAuthentication:
    """
    DEPRECATED: Do not use.
    """
    username: str
    password: str

    def __init__(self, username: str, password: str):
        warnings.warn(DeprecationWarning("Deprecated: do not use"))

        # Need to use __setattr__ on object since dataclass is frozen
        object.__setattr__(self, "username", username)
        object.__setattr__(self, "password", password)

def __getattr__(name: str) -> object: # pragma: no cover
    """
    Handle accessing deprecated module attributes.
    """
    if name == "TIMEOUT":
        warnings.warn(DeprecationWarning("Deprecated: do not use"), stacklevel=1)
        return 3000 # Return the last value TIMEOUT had before deprecation

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
