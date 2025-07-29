"""the module is made for the convenience of users to download and use"""

from .api import DDnetApi, DDstats, Status
from .enum import MasterEnum
from .cache import CacheABC, EmptyCache, MemoryCache
from .util import slugify2
from .scheme import *  # noqa: F403

__version__ = "0.14.2"
__author__ = "ByFox"
__LICENSE__ = "MIT"
