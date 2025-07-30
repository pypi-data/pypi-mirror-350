import os
import re
import sys

sys.path.insert(0, re.sub(r"([\\/]items)|([\\/]spiders)", "", os.getcwd()))

__all__ = [
    "Spider",
    "Item",
    "Request",
    "Response",
    "helpers",
    "const",
    "Logging",
    "Setting",
    "AiohttpDownloader",
    "HttpxDownloader",
]

from hoopa.core.spider import RedisSpider, Spider
from hoopa.downloader import AiohttpDownloader, HttpxDownloader
from hoopa.item import Item
from hoopa.request import Request
from hoopa.response import Response
from hoopa.settings import const
from hoopa.utils import helpers
from hoopa.utils.log import Logging
from hoopa.utils.project import Setting

__version__ = "0.1.12"
