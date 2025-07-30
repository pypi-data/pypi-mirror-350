"""
Time-series client & related types
"""
from collections.abc import Mapping, Sequence
from typing import Any, TypeAlias

from pymongo.command_cursor import CommandCursor

from ixoncdkingress.function._collection import Collection

_EntryType: TypeAlias = Mapping[str, object]


class TimeSeriesClient(Collection[_EntryType]):
    """
    Client for a Time Series collection.
    """

    def aggregate(self, pipeline: Sequence[Mapping[str, Any]]) -> CommandCursor[_EntryType]:
        """
        Run the given aggregation pipeline against the collection
        """
        return self._collection.aggregate(pipeline)
