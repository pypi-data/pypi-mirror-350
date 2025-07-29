"""the module is made for the convenience of users to download and use"""

from .api import DDnetApi, DDstats, Status
from .enum import MasterEnum
from .cache import CacheABC, EmptyCache, MemoryCache
from .scheme import *  # noqa: F403

__version__ = "0.14.0"
__author__ = "ByFox"
__LICENSE__ = "MIT"
