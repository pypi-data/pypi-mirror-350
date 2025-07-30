"""
此模块管理本库的运行时配置。包括：
- 管理语言配置
使用 update_config 更新配置，更新配置之后使用 load_config 加载最新的配置。
- 翻译配置
load_config 加载好的配置可以借助rc(Runtime Config)使用。
使用 rc.set_language 设置语言。
使用 rc.translate 获取当前语言的翻译文本。
"""

__all__ = [
    "load_config",
    "update_config",
    "set_language",
    "rc",
]

import warnings
from collections import defaultdict, deque
from typing import TextIO, Type, TYPE_CHECKING, Optional

from kawaiitb._default_config import DEFAULT_CONFIG, EXTENDED
from kawaiitb.utils import readables

if TYPE_CHECKING:
    from kawaiitb.kwihandler import ErrorSuggestHandler

_config = DEFAULT_CONFIG.copy()


def update_config(config_data: dict):
    _config["translate_keys"] |= config_data["translate_keys"]
    _config["default_lang"] = config_data.get("default_lang", _config["default_lang"])


def load_config(config: dict | TextIO = None):
    """
    加载配置文件. 可以加载dict.
    """
    global _config
    if config is not None:
        if isinstance(config, readables):
            import json
            config_data = json.load(config)
        elif isinstance(config, dict):
            config_data = config
        else:
            raise TypeError("[KawaiiTB] config must be a dict or a file-like object")
        update_config(config_data)

    # 验证继承合法性
    for lang, data in _config["translate_keys"].items():
        if "extend" in data:
            extend_lang = data["extend"]
            if extend_lang not in _config["translate_keys"]:
                warnings.warn(f"[KawaiiTB] Language {extend_lang} is not supported, using default language instead.")
                _config["translate_keys"][lang]["extend"] = "default"
        elif lang != "default":
            _config["translate_keys"][lang]["extend"] = "default"

    # 验证非环 (Kahn法)
    adjacency = defaultdict(list)
    in_degree = defaultdict(int)
    for lang, data in _config["translate_keys"].items():
        if "extend" not in data:
            continue
        parent_lang = data["extend"]
        adjacency[parent_lang].append(lang)
        in_degree[lang] += 1
    queue = deque()
    for lang in _config["translate_keys"]:
        if in_degree[lang] == 0:
            queue.append(lang)
    processed = 0
    while queue:
        current = queue.popleft()
        processed += 1
        for neighbor in adjacency[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    if processed != len(_config["translate_keys"]):
        raise Exception("[KawaiiTB] A circular dependency exists in the language configuration!")

    # 重置默认语言
    if "rc" in globals():
        rc.change_language(_config["default_lang"])


def set_language(lang: str):
    rc.change_language(lang)


MAX_EXTEND_DEPTH = 10  # 最大继承深度


class RuntimeConfig:
    global _config

    def __init__(self):
        # 语言不一定非要是现存语言，也可以是额外的自定义提示信息(比如猫娘提示)
        self._lang = _config["default_lang"]
        self.langs = _config["translate_keys"].keys()
        self.default_config = _config["translate_keys"]["default"]
        self.handlers = []

    def register_handler(self, Handler: Type["ErrorSuggestHandler"]):
        """注册处理器的翻译键."""
        transkeys = Handler.translation_keys()
        if transkeys is not None and len(transkeys) > 0:
            for lang, data in transkeys.items():
                if lang not in _config["translate_keys"]:
                    _config["translate_keys"][lang] = {}
                _config["translate_keys"][lang] |= data
            load_config()

    def _get_key(self, lang, key):
        return _config["translate_keys"][lang][key]

    def _check_key(self, lang, key):
        return key in _config["translate_keys"][lang]

    def _check_lang(self, lang):
        return lang in self.langs

    def change_language(self, lang: str):
        if not self._check_lang(lang):
            warnings.warn(f"[KawaiiTB] Language {lang} is not exist, using default language instead.")
            self._lang = "default"
        else:
            self._lang = lang

    def translate(self, key: str, /, **kwargs):
        lang = self._lang
        depth_out = True
        for _ in range(MAX_EXTEND_DEPTH):
            if not self._check_lang(lang):  # 检查所选的语言是否存在, 否则使用默认语言
                warnings.warn(f"[KawaiiTB] Language {lang} is not exist, using default language instead.")
                warnings.warn('langs:' + str(self.langs))
                lang = "default"
                continue

            if self._check_key(lang, key) \
                    and self._get_key(lang, key) != EXTENDED:  # 优先使用该语言已有的配置
                if kwargs:
                    return self._get_key(lang, key).format(**kwargs)
                return self._get_key(lang, key)

            if lang == "default":  # 如果连默认配置都不存在这个键，返回未知配置提示
                warnings.warn(f"[KawaiiTB] Unknown translate key: {key}")
                return f"<Unknown config: {key}>"

            if self._check_key(lang, "extend"):  # 如果继承自其他语言……
                lang = self._get_key(lang, "extend")
                continue

            # 其他情况，走默认配置
            lang = "default"

        warnings.warn(f"[KawaiiTB] Exceeded maximum extend depth for key: {key}")
        return f"<[KawaiiTB] Unreachable translate key: {key}>"

    def anchors(self, indent: str, left_start: int, left_end: int, right_start: int, right_end: int, crlf: bool):
        primary = self.translate("config.anchor.primary")
        secondary = self.translate("config.anchor.secondary")

        left_segment = primary * (left_end - left_start)
        middle_segment = secondary * (right_start - left_end)
        right_segment = primary * (right_end - right_start)
        suffix = self.translate("config.anchor.suffix")
        if crlf:
            suffix += "\n"

        return indent + left_segment + middle_segment + right_segment + suffix

    def exc_line(self, exc_type_str: str, exc_value_str: Optional[str]=None):
        if exc_value_str is None:
            return self.translate("exception.exc_line_noval", etype=exc_type_str)
        else:
            return self.translate("exception.exc_line", etype=exc_type_str, value=exc_value_str)

rc: RuntimeConfig = RuntimeConfig()
