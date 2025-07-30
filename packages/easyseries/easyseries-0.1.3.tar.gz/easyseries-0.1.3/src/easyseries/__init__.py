"""EasySeries - A comprehensive HTTP utility toolkit built on httpx."""

__version__ = "0.1.3"
__author__ = "Marvin Guo"
__email__ = "support@memolog.us"

from easyseries.core.config import Settings
from easyseries.core.exceptions import EasySeriesError
from easyseries.http.client import HTTPClient

__all__ = [
    "EasySeriesError",
    "HTTPClient",
    "Settings",
    "__version__",
]
