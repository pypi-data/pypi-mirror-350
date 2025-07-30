"""
这里定义错误处理器的基类，动态扩展的示例将在这里展示。
"""
import linecache
from types import TracebackType
from typing import Generator, Any, Type, final

import astroid

from kawaiitb.kraceback import KTBException, FrameSummary
from kawaiitb.runtimeconfig import rc
from kawaiitb.utils.ast_parse import astroid_walk_inside

__all__ = [
    "ErrorSuggestHandler"
]

@KTBException.register
class ErrorSuggestHandler:
    """
    异常处理器的基类。

    优先级最高的处理器会最先认领异常。
    在KTBException初始化时会顺带初始化所有的处理器。
    在格式化时，KTBException传入自身并判断各处理器是否能处理异常，然后选择优先级最高的处理器。

    优先级原则：
    - 仅ErrorSuggestHandler父类使用0.0优先级。低于此优先级的均不可能认领。
    - 原生级处理器使用1.0优先级。即本文件中的所有附加处理器。
    - 希望官方处理器先认领，认领失败时自己处理时，使用属于(0, 1)的优先级。
    - 希望自己的处理器先认领，认领失败时官方处理器处理时，使用属于(1, +infny)的优先级。
        - 独立的异常类型，使用优先级2
          (如ModuleNotFoundErrorHandler专注于ModuleNotFoundError)。
        - 独立的异常描述级别的，使用优先级3
          (如NoneTypeErrorHandler处理参数为None的TypeError)。
        - 针对特定异常参数/信息的建议/翻译，使用优先级4
          (如PyyamlNotFoundErrorHandler处理pyyaml的NameError)。
    """

    __priority__: float = 0.0  # 基处理器的优先级为0.0
    # 所有有效的处理器都应该高于此优先级以覆盖处理。
    # 所有不生效(如仅翻译)的处理器都应该低于此优先级。建议使用标准的: -1.0.

    def __init__(self, exc_type: Type[BaseException], exc_value: BaseException, exc_traceback: TracebackType, *, limit=None,
                 lookup_lines=True, capture_locals=False, compact=False,
                 max_group_width=15, max_group_depth=10, _seen=None):
        ...
        # 此处可以添加一些初始化逻辑，比如确定自己能不能处理这个异常。
        # 也可以根据这个异常帧的信息处理一些值。
        # 上面传入的东西就是一个异常发生时所有传给你的信息，包括异常的语句，上下文代码，这这那那的。
        # 可以看一些预设的处理器了解一下如何处理这些信息。

        # 另外，如果你是直接继承的ErrorSuggestHandler，其实可以省略super调用，
        # 因为init实际上并没有做什么……

        # 如果也不需要后面的设置，可以用**kwargs来收取所有参数，然后按需提取和忽略。、

    def __init_subclass__(cls, priority):
        """
        初始化子类时，自动注册翻译键。
        可以通过priority参数来设置处理器的优先级。
>>> class MyHandler(ErrorSuggestHandler, priority=2.0):
>>>     ...
        """
        cls.__priority__ = priority

    @property
    def priority(self) -> float:
        return self.__priority__

    def can_handle(self, ktb_exc: KTBException) -> bool:
        """返回本处理器是否能处理异常。"""
        # 处理器接受异常需要满足以下条件：
        # 1. 处理器声明自己能处理异常。
        # 2. 没有更高优先级的处理器能处理异常。
        # 举例来说，ModuleNotFoundErrorHandler和PyyamlNotFoundErrorHandler都能处理`import pyyaml`
        # 但前者只是基本的找不到包提醒，后者则是提供了更详细的解决方案，提示用户应该导入的是yaml。
        # 所以优先级PyyamlNotFoundErrorHandler(4.0) > ModuleNotFoundErrorHandler(2.0)。

        return True  # 当然这里是基处理器，要处理所有异常

    @classmethod
    def translation_keys(cls) -> dict[str, dict[str, Any]]:
        """
        翻译键。
        每个处理器都可以有自己的翻译键，建议非官方逻辑的处理器使用"exthandler.<namespace>.xxx"命名翻译键。
        返回格式是标准的静态文件格式，即{<language>: {<key>: <value>}}。
        **如果非空，则必须有"default"键**。

        如果你希望单纯翻译一个自定义处理器，你可以定义一个优先级为-1的处理器，然后在其中定义翻译键并注册。
        """
        ...

    def handle(self, etype: KTBException) -> Generator[str, None, None]:
        """
        处理异常，返回一个生成器，生成器会逐行产生处理后的错误信息。
        并不一定非要每行一定断一下，这只是为了模块的灵活性，如果你需要输出确定不变的多行信息，直接写就是了。
        """
        stype = etype.exc_type.__qualname__
        smod = etype.exc_type.__module__
        if smod not in ("__main__", "builtins"):
            if not isinstance(smod, str):
                smod = "<unknown>"
            stype = smod + '.' + stype
        yield rc.exc_line(stype, etype.final_exc_str)

    @staticmethod
    @final
    def parse_ast_from_exc(exc_frame: FrameSummary, parse_line=False):
        """
        从一个帧中解析并产生相关的AST节点
        """
        start_line = exc_frame.lineno
        end_line = exc_frame.end_lineno
        start_col = 0 if parse_line else exc_frame.colno
        end_col = 99999999 if parse_line else exc_frame.end_colno
        tree = astroid.parse("".join(linecache.getlines(exc_frame.filename)))

        yield from astroid_walk_inside(tree, start_line, end_line, start_col, end_col)




# 以下是示例代码
class ImportErrorHandler(ErrorSuggestHandler, priority=2.0):
    ...

#@KTBException.register 使用装饰器可以注册处理器。本示例中暂不使用。
class PyYamlImportErrorHandler(ImportErrorHandler, priority=4.0):
    """
    在pyyaml导入失败时提供更详细的解决方案。

    一个Handler将在KTBException初始化时被初始化
    初始化时，__init__会被传入异常的所有原始参数
    (不需要的参数可以用**kwargs原样丢回super)
    之后，KTBException会调用can_handle来判断是否能处理异常
    如果最终以最高优先级被选中，则会调用handle来处理异常
    """
    def __init__(self, exc_type, exc_value, exc_traceback, **kwargs):
        super().__init__(exc_type, exc_value, exc_traceback, **kwargs)

        # 检查是否是pyyaml相关的导入错误
        # 这里从__init__接受的参数的一部分也可以在后面从KTBException中获取,
        # 但其中的一些参数可能会在处理时被修改，所以最好还是从这里获取。
        # 如果需要修改后的参数，可以在handle中获取。

        self._can_handle = (issubclass(exc_type, ImportError) and
                            getattr(exc_value, "name", "") == "pyyaml")

    # 注册扩展翻译键到运行时配置，以供后续使用
    @classmethod
    def translation_keys(cls):
        return {
            "default": {
                # 没必要分行yield，直接写多行文本就好了~！
                "exthandler.pyyaml.hint": "Attention: You may have installed the 'pyyaml' package, but you should import 'yaml' instead of 'pyyaml'.\n"
                                          "- Install pyyaml using pip: pip install pyyaml\n"
                                          "- Import yaml in your code: import yaml",
            },
            "zh_hans": {
                "exthandler.pyyaml.hint": "注意：你可能已经安装了pyyaml包，但导入时应该使用'yaml'而不是'pyyaml'。\n"
                                          "- 使用pip安装pyyaml: pip install pyyaml\n"
                                          "- 在代码中导入yaml: import yaml",
            }
        }

    def can_handle(self, ktb_exc) -> bool:
        # 因为__init__和can_handle都是每个handle的必经之路
        # 所以在那边存储在这处理和直接在那处理保存结果效率都差不多
        return self._can_handle

    def handle(self, ktb_exc) -> Generator[str, None, None]:
        """
        1. 继承原则
        在本测试用例PyYamlImportErrorHandler中,
        如果直接继承 ErrorSuggestHandler 会导致
        super处理时直接把"ImportError: No module named 'pyyaml'"
        这条原生信息直接丢给用户. 而 ImportErrorHandler一定会为此准备。
        即使你不打算使用 ImportErrorHandler 提供的信息
        我仍然建议你继承 ImportErrorHandler, 这可以使得逻辑更清晰
        也可以避免一些潜在问题.
        2. 翻译原则
        你可以使用 rc.translate 来获取翻译, 也可以直接硬编码.
        但我强烈建议你使用翻译, 并至少准备default的英语语种.
        这样你的代码可以令全世界程序员都能看懂.
        3. yield原则
        如上, __init__和can_handle都是每个handle的必经之路,
        但只有handle是处理器确定要处理异常时才会被调用.
        只有在handle中, 你才能处理一些真正耗时的部分,
        比如复杂的ast解析等.
        大量的处理器在初始化时一个个做这件事是很不划算的.
        """
        yield from super().handle(ktb_exc)
        yield rc.translate("exthandler.pyyaml.hint") + "\n"