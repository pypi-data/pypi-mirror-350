"""
This file is used to load KawaiiTB with a single command.
Usage:
>>> import kawaiitb.autoload
"""

from kawaiitb.tools import load, ENV_KAWAIITB_LANG, ENV_KAWAIITB_CONF
import os
if not os.environ.get(ENV_KAWAIITB_LANG) and not os.environ.get(ENV_KAWAIITB_CONF):
    load('neko_zh')  # 喵~
else:
    load()
