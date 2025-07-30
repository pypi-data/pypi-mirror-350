"""
Kawaii Traceback - Cute Python traceback beautifier

A delightful tool for transforming standard Python tracebacks into adorable and 
user-friendly error messages with multilingual support.
"""

__version__ = "0.1.0"
__author__ = "BPuffer <mc-puffer@qq.com>"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2025 BPuffer"
__description__ = "A kawaii Python traceback beautifier with multilingual support"

import sys

import kawaiitb.kraceback as traceback
from kawaiitb.handlers import __all__ as _handlers
from kawaiitb.kraceback import KTBException
from kawaiitb.kwihandler import ErrorSuggestHandler
from kawaiitb.runtimeconfig import rc, load_config
from kawaiitb.tools import load, unload

__all__ = [
    "traceback",
    "rc",
    "load",
    "unload",
    "ErrorSuggestHandler",
    "KTBException",
    "load_config",
    *_handlers,
]