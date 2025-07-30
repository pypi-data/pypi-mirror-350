import warnings

warnings.warn(
    "ixoncdkingress.cbc has been deprecated, please use ixoncdkingress.function",
    DeprecationWarning,
)

from ixoncdkingress.function.document_db_client import (  # noqa: E402, I001
    DocumentDBAuthentication,
    DocumentDBClient,
    DocumentType,
    TIMEOUT,
)

__all__ = ["DocumentDBAuthentication", "DocumentDBClient", "DocumentType", "TIMEOUT"]
