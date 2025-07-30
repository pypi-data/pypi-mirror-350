import warnings

warnings.warn(
    "ixoncdkingress.cbc has been deprecated, please use ixoncdkingress.function",
    DeprecationWarning,
)

from ixoncdkingress.function.api_client import ApiClient # noqa: E402, I001

__all__ = ["ApiClient"]
