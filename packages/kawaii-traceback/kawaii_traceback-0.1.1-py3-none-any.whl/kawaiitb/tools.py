import os
import sys
from functools import wraps
from traceback import format_exception as orig_format_exception
from typing import overload, Optional, Literal

from kawaiitb.kraceback import KTBException
from kawaiitb.runtimeconfig import rc, load_config
from kawaiitb.utils.fromtraceback import parse_value_tb, sentinel as _sentinel
from kawaiitb.utils import SupportsReading, readables

ENV_KAWAIITB_LANG = "KAWAIITB_LANG"
ENV_KAWAIITB_CONF = "KAWAIITB_CONF"

__excepthook__ = sys.excepthook
__in_console__ = hasattr(sys, 'ps1')
if __in_console__:
    __ps1__ = sys.ps1
    __ps2__ = sys.ps2


def unload():
    sys.excepthook = __excepthook__
    if __in_console__:
        sys.ps1 = __ps1__
        sys.ps2 = __ps2__


@overload
def load(*, excepthook: bool = True, console_prompt: bool = True):
    """加载默认配置"""


@overload
def load(lang: str = None, *, excepthook: bool = True, console_prompt: bool = True):
    """选取一个语言"""


@overload
def load(file: SupportsReading = None, *, excepthook: bool = True, console_prompt: bool = True,
         encoding: Optional[str] = 'utf-8'):
    """加载一个配置文件"""


@overload
def load(lang: Literal[None] = None, filename: str = None, *, excepthook: bool = True, console_prompt: bool = True,
         encoding: Optional[str] = 'utf-8'):
    """从文件名加载一个配置文件"""


@overload
def load(lang: str = None, file: SupportsReading | str = None, *, excepthook: bool = True, console_prompt: bool = True,
         encoding: Optional[str] = 'utf-8'):
    """加载一个配置文件并选择一个语言"""


def load(lang: Optional[SupportsReading | str] = None,
         file: Optional[SupportsReading | str] = None,
         *,
         excepthook: bool = True,
         console_prompt: bool = True,
         encoding: Optional[str] = 'utf-8',
         ):
    """
    加载配置并劫持hook.

    :param lang: 要加载的语言. 如果为None, 则加载默认配置.
    :param file: 配置文件. 如果为None, 则加载默认配置.
    :param excepthook: 是否劫持sys.excepthook. 默认值为True.
    :param console_prompt: 是否劫持控制台提示符. 默认值为True.
    :param encoding: 配置文件的编码. 默认值为'utf-8'.

    usage:
>>> import kawaiitb
>>> kawaiitb.load()  # 加载默认配置。读取环境变量KAWAIITB_LANG和KAWAIITB_CONF
>>> kawaiitb.load('neko_zh')  # 加载指定语言的配置
>>> kawaiitb.load(file='my_conf.json')  # 加载指定文件的配置
>>> kawaiitb.load('present1', 'hot_conf.json')  # 加载指定语言和文件的配置
>>> with open('my_conf.json') as f:
...     load(f)  # 加载指定文件的配置
>>> with open('hot_conf.json') as f:
...     load('present1', f)  # 加载指定语言和文件的配置
    """
    if isinstance(lang, readables) and file is None:
        lang, file = None, lang  # When call with a single file-like object, same as load(file=...)
    if not isinstance(lang, (str, type(None))):
        raise ValueError(f"Invalid type of lang {type(lang)}")
    if not isinstance(file, (str, type(None), *readables)):
        raise ValueError(f"Invalid type of file {type(file)}")

    # 默认情况: load()
    if lang is None and file is None:
        load_config()
        if ENV_KAWAIITB_LANG in os.environ:
            rc.change_language(os.environ[ENV_KAWAIITB_LANG])

        if ENV_KAWAIITB_CONF in os.environ:
            with open(os.environ[ENV_KAWAIITB_CONF], 'r', encoding=encoding) as f:
                load_config(f)
        override(excepthook=excepthook, console_prompt=console_prompt)
        return

    # 用法: load('neko_zh')
    if isinstance(lang, str) and file is None:
        load_config()
        rc.change_language(lang)
        override(excepthook=excepthook, console_prompt=console_prompt)
        return

    # 用法: load(file='my_conf.json')
    if lang is None and isinstance(file, str):
        with open(file, 'r', encoding=encoding) as f:
            load_config(f)
        override(excepthook=excepthook, console_prompt=console_prompt)
        return

    # 用法: load('present1', 'hot_conf.json')
    if isinstance(lang, str) and isinstance(file, str):
        with open(file, 'r', encoding=encoding) as f:
            load_config(f)
        rc.change_language(lang)
        override(excepthook=excepthook, console_prompt=console_prompt)
        return

    # 用法: with open('my_conf.json') as f: load(f)
    if lang is None and hasattr(file, 'readable') and file.readable():
        load_config(file)
        override(excepthook=excepthook, console_prompt=console_prompt)
        return

    # 用法: with open('hot_conf.json') as f: load(f, 'present1')
    if isinstance(lang, str) and hasattr(file, 'readable') and file.readable():
        load_config(file)
        rc.change_language(lang)
        override(excepthook=excepthook, console_prompt=console_prompt)
        return

    raise ValueError("Invalid arguments")


def override(excepthook=True, console_prompt=None):
    if excepthook:
        @wraps(orig_format_exception)  # 签名对齐 traceback.format_exception
        def wrapped(exc, /, value=_sentinel, tb=_sentinel, limit=None, chain=True):
            try:
                value, tb = parse_value_tb(exc, value, tb)
                te = KTBException(type(value), value, tb, limit=limit, compact=True)
                return list(te.format(chain=chain))
            except Exception as ktb_self_raised_exc:
                return orig_format_exception(exc, value=_sentinel, tb=_sentinel, limit=None, chain=True) + [
                    "\n\nKawaiiTB occurred another exception while formatting this exception:\n"
                ] + list(orig_format_exception(ktb_self_raised_exc)) + [
                    "Please report this to the KawaiiTB developers.\n"
                ]

        sys.excepthook = lambda etype, value, tb: sys.stderr.write(''.join(wrapped(etype, value, tb)))

    if (
            console_prompt is True and
            __in_console__ and
            (ps1 := rc.translate("config.prompt1")) and
            (ps2 := rc.translate("config.prompt2"))
    ):
        sys.ps1 = ps1
        sys.ps2 = ps2
