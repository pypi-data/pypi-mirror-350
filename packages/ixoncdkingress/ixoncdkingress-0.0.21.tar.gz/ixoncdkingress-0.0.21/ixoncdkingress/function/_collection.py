"""
Functionality shared between all sorts of collections
"""
from collections.abc import Mapping
from typing import Any, Generic, TypeVar

from pymongo.collection import Collection as MongoCollection
from pymongo.cursor import Cursor

_T = TypeVar("_T", bound=Mapping[str, object])

class Collection(Generic[_T]):
    """
    A read-only collection of data.
    """
    _collection: MongoCollection[_T]

    def __init__(
            self,
            collection: MongoCollection[_T],
    ) -> None:
        self._collection = collection

    def find_one(
            self, *args: Any, filter_map: Any | None, **kwargs: Any
    ) -> _T | None:
        """
        Get a single item from the collection.
        """
        return self._collection.find_one(filter_map, *args, **kwargs)

    def find(self, *args: Any, **kwargs: Any) -> Cursor[_T]:
        """
        Query the collection.
        """
        return self._collection.find(*args, **kwargs)

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__}'
            f' company={self._collection.database.name},'
            '>'
        )
