import warnings

warnings.warn(
    "ixoncdkingress.cbc has been deprecated, please use ixoncdkingress.function",
    DeprecationWarning,
)

from ixoncdkingress.function.objectstorage.types import ( # noqa: E402, I001
    ListPathResponse,
    PathData,
    PathMapping,
    PathResponse,
    ResourceType,
)

__all__ = [
    "ListPathResponse",
    "PathData",
    "PathMapping",
    "PathResponse",
    "ResourceType",
]
