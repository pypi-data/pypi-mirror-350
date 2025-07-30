from .sdk import SploreSDK, AgentSDK

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version("splore_sdk")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["SploreSDK", "AgentSDK", "__version__"]
