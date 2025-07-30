"""
Types that can be used when implementing
the Object Storage interface.

Compatible with ayayot.objectstorage_v1
"""

import enum
from typing import Literal, TypedDict


class ResourceType(str, enum.Enum):
    """
    A type of resource for which a path is returned
    """
    ASSET = 'Asset'
    AGENT = 'Agent'

class PathData(TypedDict, total=True):
    """
    Response data for a single path
    """
    path: str

class PathMapping(TypedDict, total=True):
    """
    A mapping between a certain resource and a path,
    as returned by authorize_list
    """
    publicId: str | None
    path: str
    type: ResourceType

class PathResponse(TypedDict, total=True):
    """
    The expected type for a response for the
    Object Storage authorize_upload, authorize_download &
    authorize_delete APIs
    """
    result: Literal['success']
    data: PathData

class ListPathResponse(TypedDict, total=True):
    """
    The expected type for a response for the
    Object Storage authorize_list API
    """
    result: Literal['success']
    data: list[PathMapping]
