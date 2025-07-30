import sys
from typing import Generator

import astroid

from kawaiitb.kraceback import KTBException
from kawaiitb.kwihandler import ErrorSuggestHandler
from kawaiitb.runtimeconfig import rc
from kawaiitb.utils import safe_string
from kawaiitb.utils.fromtraceback import compute_suggestion_error

__all__ = [
    "SyntaxErrorSuggestHandler",
    "ImportErrorSuggestHandler",
    "NameAttributeErrorSuggestHandler",
    # 这些属于原生增强，优先级都是1.1

]


@KTBException.register
class SyntaxErrorSuggestHandler(ErrorSuggestHandler, priority=1.1):
    """
    本处理器模仿原生的语法错误处理器，为语法错误添加额外的锚点指示
    """

    def __init__(self, exc_type, exc_value, exc_traceback, *, limit=None,
                 lookup_lines=True, capture_locals=False, compact=False,
                 max_group_width=15, max_group_depth=10, _seen=None):
        super().__init__(exc_type, exc_value, exc_traceback)
        if exc_type and issubclass(exc_type, SyntaxError):
            exc_value: SyntaxError
            self.filename = exc_value.filename
            lno = exc_value.lineno
            self.lineno = str(lno) if lno is not None else None
            end_lno = exc_value.end_lineno
            self.end_lineno = str(end_lno) if end_lno is not None else None
            self.text = exc_value.text
            self.offset = exc_value.offset
            self.end_offset = exc_value.end_offset
            self.msg = exc_value.msg

    @classmethod
    def translation_keys(cls):
        return {}  # 翻译键均由默认配置提供，不需要额外的翻译键

    def can_handle(self, ktb_exc) -> bool:
        return issubclass(ktb_exc.exc_type, SyntaxError)

    def handle(self, ktb_exc) -> Generator[str, None, None]:
        r"""
        (-) Traceback (most recent call last):
        (-)   File "C:\Users\BPuffer\Desktop\kawaii-traceback\main.py", line 139:8, in <module>
        (-)     exec("what can i say?")
        (1)   File "<string>", line 1
        (2)     what can i say?
        (3)          ^^^
        (4) SyntaxError: invalid syntax (<string>, line 1)
        """
        if self.lineno is not None:
            # part (1)
            yield rc.translate("frame.location.without_name",
                               file=self.filename or "<string>",  # repr转义
                               lineno=self.lineno, )

        text = self.text
        if text is not None:
            rtext = text.rstrip('\n')
            ltext = rtext.lstrip(' \n\f')
            spaces = len(rtext) - len(ltext)
            # part (2)
            yield rc.translate("frame.location.linetext",
                               line=ltext)

            if self.offset is not None:
                offset = self.offset
                end_offset = self.end_offset if self.end_offset not in {None, 0} else offset
                if offset == end_offset or end_offset == -1:
                    end_offset = offset + 1

                colno = offset - 1 - spaces
                end_colno = end_offset - 1 - spaces
                if colno >= 0:
                    # part (3)
                    # caretspace = ((c if c.isspace() else ' ') for c in ltext[:colno])
                    # yield '    {}{}'.format("".join(caretspace), ('^' * (end_colno - colno) + "\n"))
                    anchor_len = end_colno - colno
                    yield rc.anchors('    ' + ' ' * colno, 0, 0, anchor_len, anchor_len, crlf=True)

        msg = self.msg or "<no detail available>"
        # part (4)
        yield from super().handle(ktb_exc)


@KTBException.register
class ImportErrorSuggestHandler(ErrorSuggestHandler, priority=1.1):
    """
    本处理器模仿原生的ImportError的拼写错误检测
    为导入中的拼写错误添加额外的正确拼写提示
    """

    def __init__(self, exc_type, exc_value, exc_traceback, *, limit=None,
                 lookup_lines=True, capture_locals=False, compact=False,
                 max_group_width=15, max_group_depth=10, _seen=None):
        super().__init__(exc_type, exc_value, exc_traceback)

        self._can_handle = issubclass(exc_type, ImportError) and getattr(exc_value, "name_from", None) is not None

        self.suggestion = None
        if self._can_handle:
            self.wrong_name = getattr(exc_value, "name_from")
            self.suggestion = compute_suggestion_error(exc_value, exc_traceback, self.wrong_name)

    def can_handle(self, ktb_exc) -> bool:
        return self._can_handle

    @classmethod
    def translation_keys(cls):
        return {
            "default": {
                "native.import_error_suggestion.hint": "Did you mean '{suggestion}'?",
            },
            "zh_hans": {
                "native.import_error_suggestion.hint": "你可能是想导入'{suggestion}'",
            }
        }

    def handle(self, ktb_exc) -> Generator[str, None, None]:
        yield from super().handle(ktb_exc)
        if self.suggestion:
            yield rc.translate("native.import_error_suggestion.hint", suggestion=self.suggestion)


@KTBException.register
class NameAttributeErrorSuggestHandler(ErrorSuggestHandler, priority=1.1):
    """
    本处理器模仿原生的NameError的拼写错误检测
    为NameError的拼写错误添加额外的正确拼写提示
    并为存在于标准库和第三方库中的名字添加额外的提示
    """

    def __init__(self, exc_type, exc_value, exc_traceback, *, limit=None,
                 lookup_lines=True, capture_locals=False, compact=False,
                 max_group_width=15, max_group_depth=10, _seen=None):
        super().__init__(exc_type, exc_value, exc_traceback)

        self._can_handle = (issubclass(exc_type, (NameError, AttributeError)) and
                            getattr(exc_value, "name", None) is not None)

        if self._can_handle:
            self.wrong_name = getattr(exc_value, "name")
            self.suggestion = compute_suggestion_error(exc_value, exc_traceback, self.wrong_name)
            self.is_stdlib = self.wrong_name in sys.stdlib_module_names

            self.is_3rd_party = False
            import importlib.metadata
            try:
                importlib.metadata.distribution(self.wrong_name)
                self.is_3rd_party = True
            except importlib.metadata.PackageNotFoundError:
                pass

            self.is_lib = self.is_stdlib or self.is_3rd_party

    def can_handle(self, ktb_exc) -> bool:
        return self._can_handle

    @classmethod
    def translation_keys(cls):
        return {
            "default": {
                "native.nameattr_error_suggestion.typo": "Did you mean '{suggestion}'?",
                "native.nameattr_error_suggestion.forget_import": "You may forget to import '{wrong_name}'",
                "native.nameattr_error_suggestion.or_forget_import": "or you may forget to import '{wrong_name}'",
            },
            "zh_hans": {
                "native.nameattr_error_suggestion.typo": "你是不是想输入'{suggestion}'？",
                "native.nameattr_error_suggestion.forget_import": "你可能忘记导入'{wrong_name}'了",
                "native.nameattr_error_suggestion.or_forget_import": "或者你可能忘记导入'{wrong_name}'了",
            }
        }

    def handle(self, ktb_exc) -> Generator[str, None, None]:
        yield from super().handle(ktb_exc)
        if self.suggestion:
            yield rc.translate("native.nameattr_error_suggestion.typo", suggestion=self.suggestion)

        if issubclass(ktb_exc.exc_type, NameError) and self.is_stdlib:
            if self.suggestion:
                yield rc.translate("native.nameattr_error_suggestion.or_forget_import", wrong_name=self.wrong_name)
            else:
                yield rc.translate("native.nameattr_error_suggestion.forget_import", wrong_name=self.wrong_name)

# 以上是所有原生处理中含有新增的处理逻辑的处理器。优先级均为1.1。


@KTBException.register
class StopIterationHandler(ErrorSuggestHandler, priority=1.0):  # 原生
    """
    StopIteration异常处理器
    ```
>>> def f():
>>>     for i in range(10):
>>>         yield i
>>>     return "Boom!"
>>>
>>> g = f()
>>> while True:
>>>     next(g)

... Traceback (most recent call last):
...   File "main.py", line 139, in <module>
...     next(g)
(-) StopIteration: Boom!

    改为:

(1) [StopIteration] 生成器'g'停止迭代: Boom!
    ```
    """

    def __init__(self, exc_type, exc_value, exc_traceback, **kwargs):
        super().__init__(exc_type, exc_value, exc_traceback, **kwargs)
        self._can_handle = issubclass(exc_type, StopIteration)
        if not self._can_handle:
            return

        # Python 3.7 之后，对于使用return 关键字的生成器，抛出的StopIteration异常会包含 return 的值。
        self.return_value = exc_value.value if hasattr(exc_value, 'value') else None


    def can_handle(self, ktb_exc) -> bool:
        return self._can_handle

    @classmethod
    def translation_keys(cls):
        return {
            "default": {
                "native.StopIteration.hint": "Generator '{generator}' stopped iterating.",
                "native.StopIteration.hint_with_return": "Generator '{generator}' stopped: {ret}",
            },
            "zh_hans": {
                "native.StopIteration.hint": "生成器'{generator}'没有更多值了。",
                "native.StopIteration.hint_with_return": "生成器'{generator}'没有更多值了: {ret}",
            }
        }

    def handle(self, ktb_exc: KTBException) -> Generator[str, None, None]:
        # 从栈帧中获取生成器在代码里的名称
        self.generator = "<...>"
        if len(ktb_exc.stack) > 0:
            exc_frame = ktb_exc.stack[0]
            for node in self.parse_ast_from_exc(exc_frame):
                # case: next(g) -> Call(
                #     func=Name(name=next),
                #     args=[...])
                if (
                        isinstance(node, astroid.Call) and  # 是函数调用
                        isinstance(node.func, astroid.Name) and  # 是显式函数名
                        node.func.name == 'next'  # 是next调用
                ):
                    self.generator = node.args[0].as_string()
                    break

                # case: g.__next__() -> Call(
                #     func=Attr(
                #         expr=<?>,
                #         attrname=__next__),
                #     args=[...])
                if (
                    isinstance(node, astroid.Call) and  # 是函数调用
                    isinstance(node.func, astroid.Attribute) and  # 是属性访问
                    node.func.attrname == '__next__'  # 是__next__方法调用
                ):
                    # 获取生成器表达式字符串
                    self.generator = node.func.expr.as_string()
                    break

        if self.return_value is not None:
            hint = rc.translate("native.StopIteration.hint_with_return", generator=self.generator, ret=self.return_value)
        else:
            hint = rc.translate("native.StopIteration.hint", generator=self.generator)
        yield rc.exc_line("StopIteration", hint)


@KTBException.register
class StopAsyncIterationHandler(ErrorSuggestHandler, priority=1.0):  # 原生
    """
    StopAsyncIteration异常处理器
    ```
>>> async def f():
>>>     for i in range(10):
>>>         yield i
>>>     return "Boom!"
>>>
>>> async for i in f():
>>>     pass

... Traceback (most recent call last):
...   File "main.py", line 139, in <module>
...     async for i in f():
(-) StopAsyncIteration: Boom!

    改为:

(1) [StopAsyncIteration] 异步生成器'f'停止迭代: Boom!
    ```
    """

    def __init__(self, exc_type, exc_value, exc_traceback, **kwargs):
        super().__init__(exc_type, exc_value, exc_traceback, **kwargs)
        self._can_handle = issubclass(exc_type, StopAsyncIteration)
        if not self._can_handle:
            return

        self.return_value = exc_value.value if hasattr(exc_value, 'value') else None

    def can_handle(self, ktb_exc) -> bool:
        return self._can_handle

    @classmethod
    def translation_keys(cls):
        return {
            "default": {
                "native.StopAsyncIteration.hint": "Async generator '{generator}' stopped iterating.",
                "native.StopAsyncIteration.hint_with_return": "Async generator '{generator}' stopped: {ret}",
            },
            "zh_hans": {
                "native.StopAsyncIteration.hint": "异步生成器'{generator}'没有更多值了。",
                "native.StopAsyncIteration.hint_with_return": "异步生成器'{generator}'没有更多值了: {ret}",
            }
        }

    def handle(self, ktb_exc) -> Generator[str, None, None]:
        # 从栈帧中获取异步生成器在代码里的名称
        self.generator = "<...>"
        if len(ktb_exc.stack) > 0:
            exc_frame = ktb_exc.stack[0]
            for node in self.parse_ast_from_exc(exc_frame):
                # case: anext(g) -> Call(
                #     func=Name(name=anext),
                #     args=[...])
                if (
                    isinstance(node, astroid.Call) and  # 是函数调用
                    isinstance(node.func, astroid.Name) and  # 是显式函数名
                    node.func.name == 'anext'  # 是anext调用
                ):
                    self.generator = node.args[0].as_string()
                    break

                # case: g.__anext__() -> Call(
                #     func=Attr(
                #         expr=<?>,
                #         attrname=__anext__),
                #     args=[...])
                if (
                    isinstance(node, astroid.Call) and  # 是函数调用
                    isinstance(node.func, astroid.Attribute) and  # 是属性访问
                    node.func.attrname == '__anext__'  # 是__anext__方法调用
                ):
                    # 获取异步生成器表达式字符串
                    self.generator = node.func.expr.as_string()
                    break

                # case: async for i in g: -> AsyncFor(
                #     target=<?>,
                #     iter=<?>,
                #     body=[...])
                if isinstance(node, astroid.AsyncFor):
                    self.generator = node.iter.as_string()
                    break

        if self.return_value is not None:
            hint = rc.translate("native.StopAsyncIteration.hint_with_return",
                             generator=self.generator,
                             ret=self.return_value)
        else:
            hint = rc.translate("native.StopAsyncIteration.hint",
                             generator=self.generator)
        if self.generator:
            yield rc.exc_line("StopAsyncIteration", hint)
        else:
            yield rc.exc_line("StopAsyncIteration", hint)


@KTBException.register
class OverflowErrorHandler(ErrorSuggestHandler, priority=1.0):
    """
    OverflowError异常处理器
    ```
>>> import math
>>> math.exp(1000)

... Traceback (most recent call last):
...   File "<input>", line 1, in <module>
(-) OverflowError: math range error

    改为:

(1) [OverflowError] 溢出错误: 数学范围错误
    ```
    """

    def __init__(self, exc_type, exc_value, exc_traceback, **kwargs):
        super().__init__(exc_type, exc_value, exc_traceback, **kwargs)
        self._can_handle = issubclass(exc_type, OverflowError)
        self.err_msg_key = {
            "math range error": "native.OverflowError.msg.math_range_error",
        }.get(str(exc_value), exc_value or "native.OverflowError.msg.novalue")  # match None and ""


    def can_handle(self, ktb_exc) -> bool:
        return self._can_handle

    @classmethod
    def translation_keys(cls):
        return {
            "default": {
                "native.OverflowError.msg.novalue": "A value is too large for the given type",
                "native.OverflowError.msg.math_range_error": "math range error",
            },
            "zh_hans": {
                "native.OverflowError.msg.novalue": "数值超出了其类型所能表示的范围",
                "native.OverflowError.msg.math_range_error": "数学范围错误",
            }
        }

    def handle(self, ktb_exc) -> Generator[str, None, None]:
        self.err_msg = rc.translate(self.err_msg_key)
        yield rc.exc_line("OverflowError", self.err_msg)


@KTBException.register
class ZeroDivisionErrorHandler(ErrorSuggestHandler, priority=1.0):
    """
    ZeroDivisionError异常处理器
    ```
>>> 1 / (1 - 1)

... Traceback (most recent call last):
...   File "<input>", line 1, in <module>
(-) ZeroDivisionError: division by zero

    改为:

(1) [ZeroDivisionError] 除以零 - '(1 - 1)'的值为0
    ```
    """
    def __init__(self, exc_type, exc_value, exc_traceback, **kwargs):
        super().__init__(exc_type, exc_value, exc_traceback, **kwargs)
        self._can_handle = issubclass(exc_type, ZeroDivisionError)
        self.exc_value = exc_value
        self.stack = exc_traceback

    def can_handle(self, ktb_exc) -> bool:
        return self._can_handle

    @classmethod
    def translation_keys(cls):
        return {
            "default": {
                "native.ZeroDivisionError.msg_plain": "division by zero",
                "native.ZeroDivisionError.msg": "division by zero - '{divisor}' evaluates to 0",
                "native.ZeroDivisionError.easter_eggs":["KawaiiTraceback has been installed successfully!",
                                                         "Congratulations! You have successfully installed KawaiiTraceback!",
                                                         "You can't divide by zero! QwQ",
                                                         "Tips: TracebackException is the only Exception that cannot be raised.",
                                                         "1/0 = ∞ (in the Riemann sphere)"]
            },
            "zh_hans": {
                "native.ZeroDivisionError.msg_plain": "除以零",
                "native.ZeroDivisionError.msg": "除以零 - '{divisor}'的值为0",
                "native.ZeroDivisionError.easter_eggs": ["KawaiiTraceback安装成功!",
                                                         "恭喜你发现了Python的隐藏特性：无限能量生成器！",
                                                         "不可以除以零啦喵~(´•ω•̥`)",
                                                         "冷知识：TracebackException是唯一一个不能raise的Exception",
                                                         "1/0 = ∞ (在黎曼球面上成立)"]
            }
        }

    def handle(self, ktb_exc) -> Generator[str, None, None]:
        # 一般ZeroDivisionError的错误信息都是division by zero, 或者没有。这两种情况都可以直接用翻译
        for node in self.parse_ast_from_exc(ktb_exc.stack[0]):
            # case: 1 / 0 -> BinOp(
            #     left=Num(n=1),
            #     op=Div(),
            #     right=Num(n=0))
            if (
                isinstance(node, astroid.BinOp) and node.op == '/' and  # 是转浮点除
                isinstance(node.left, astroid.Const) and node.left.value == 1 and  # 被除数是1
                isinstance(node.right, astroid.Const) and node.right.value == 0  # 除数是0
            ):
                # 输入1/0触发彩蛋
                import random
                egg = random.choice(rc.translate("native.ZeroDivisionError.easter_eggs"))
                yield rc.exc_line("KawaiiTB", egg)
                break
            elif(
                isinstance(node, astroid.BinOp) and node.op in ('/', '//')  # 是除法
            ):
                # 这就够了。不需要太麻烦的匹配，二元操作的错误帧定位本身就很精准了
                if self.exc_value is None or \
                        safe_string(self.exc_value, "") == "division by zero" or \
                        safe_string(self.exc_value, "") == "float division by zero":
                    hint = rc.translate("native.ZeroDivisionError.msg", divisor=node.right.as_string())
                else:
                    hint = self.exc_value
                yield rc.exc_line("ZeroDivisionError", hint)
                break
        else:
            yield rc.exc_line("ZeroDivisionError", rc.translate("native.ZeroDivisionError.msg_plain"))


@KTBException.register
class AssertionErrorHandler(ErrorSuggestHandler, priority=1.0):
    """
    AssertionError异常处理器
    ```
>>> a, b = 1, 2
>>> assert a == b

... Traceback (most recent call last):
...   File "<input>", line 1, in <module>
(-) AssertionError
    改为:
(1) [AssertionError] 断言 a == b, 但是 a=1, b=2.
    ```
    """
    def __init__(self, exc_type, exc_value, exc_traceback, **kwargs):
        super().__init__(exc_type, exc_value, exc_traceback, **kwargs)
        self._can_handle = issubclass(exc_type, AssertionError)
        self.exc_value = exc_value
        self.exc_traceback = exc_traceback

    def can_handle(self, ktb_exc) -> bool:
        return self._can_handle

    @classmethod
    def translation_keys(cls):
        return {
            "default": {
                "native.AssertionError.msg": "Assertion {assertion} failed.",
                "native.AssertionError.msg_with_values": "Assertion {assertion}, but {values}."
            },
            "zh_hans": {
                "native.AssertionError.msg": "断言 {assertion} 失败。",
                "native.AssertionError.msg_with_values": "断言 {assertion}, 但是 {values}."
            }
        }

    def handle(self, ktb_exc: KTBException) -> Generator[str, None, None]:
        # 如果有信息，直接返回信息
        if (self.exc_value is not None and safe_string(self.exc_value, "") != ""
            or len(ktb_exc.stack) == 0):
            yield rc.exc_line("AssertionError", safe_string(self.exc_value, "<exception>"))
            return

        # 从栈帧中获取断言的表达式字符串
        assert_expr = None
        assert_exprs: set[str] = set()
        exc_frame = ktb_exc.stack[0]
        for node in self.parse_ast_from_exc(exc_frame, parse_line=True):
            if not isinstance(node, astroid.Assert):
                continue
            expr = node.test
            assert_expr = expr.as_string()
            if not assert_expr:
                continue
            # 收集断言表达式中的变量名
            if isinstance(expr, astroid.Compare):
                # 比较表达式: a == b, a > b > c 等
                assert_exprs.add(expr.left.as_string())
                for _, right in expr.ops:
                    assert_exprs.add(right.as_string())
                    # TODO: 支持递归的表达式
                    # 问题: 如何判断递归下的表达式是用户所需要看到的
                    # 阻力: 断言表达式通常大道至简, 甚至第二层嵌套都很少看到, 实用型存疑
            elif isinstance(expr, astroid.BoolOp):
                # 布尔运算: a and b and c 等
                assert_exprs.add(expr.as_string())
                for value in expr.values:
                    if isinstance(value, astroid.Name):
                        assert_exprs.add(value.as_string())
            elif isinstance(expr, astroid.Name):
                # 简单变量: assert a
                assert_exprs.add(expr.as_string())
            elif isinstance(expr, astroid.Call):
                # 函数调用: assert a()
                # 如果函数以"is""not""has"开头, 则取得所有函数参数, 否则只取整个表达式的值
                if isinstance(expr.func, astroid.Name):
                    func_name = expr.func.as_string().split(".")[-1]
                    if func_name.startswith(("is", "not", "has")):
                        [
                            assert_exprs.add(arg.as_string())
                            for arg in expr.args
                            if isinstance(arg, (astroid.Name, astroid.Expr))
                        ]
                        # for arg in expr.args:
                        #     assert_exprs.add(arg.as_string())
                    else:
                        assert_exprs.add(expr.as_string())
            elif isinstance(expr, (astroid.BinOp, astroid.UnaryOp)):
                # 一二元运算等直接求值, 这些变量的最终值不是布尔, 用户只需要这个值.
                for operand in [expr.left, expr.right]:
                    if isinstance(operand, astroid.Name):
                        assert_exprs.add(operand.as_string())
            break

        if assert_expr is None:
            yield rc.exc_line("AssertionError", rc.translate("native.AssertionError.msg", assertion="<Unknown Expression>"))
            return

        # 获取变量的实际值
        values = []
        frame = self.exc_traceback.tb_frame
        globals_dict = frame.f_globals
        locals_dict = frame.f_locals

        for expr_str in assert_exprs:
            try:
                evaluated = eval(expr_str, globals_dict, locals_dict)
                # 此处使用eval是因为原表达式一定已经求值成功了，才会报AssertionError
                values.append(f"{expr_str}={evaluated!r}")
            except Exception:
                # 理论上不会进入这个分支, 但安全起见.
                yield f"[KawaiiTB Error] strange error when eval {expr_str}"

        values_str = ", ".join(values)
        if len(values_str) > 50:
            values_str = values_str[:50] + "..."

        if values:
            yield rc.exc_line(
                "AssertionError",
                rc.translate("native.AssertionError.msg_with_values",
                             assertion=assert_expr,
                             values=", ".join(values)))
        else:
            yield rc.exc_line(
                "AssertionError",
                rc.translate(
                    "native.AssertionError.msg",
                    assertion=assert_expr
                )
            )




TODOS = {
    "BaseException": {
        "BaseException": "不设计。这个异常过于抽象，基本没人会单独抛",
        "SystemExit": "SystemExitHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
        "KeyboardInterrupt": "KeyboardInterruptHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
        "GeneratorExit": "不要设计，因为这个异常不会被显示",
        "Exception": {
            "Exception": "不设计。这个异常过于抽象，基本没人会单独抛",
            "StopIteration": "StopIterationHandler(ErrorSuggestHandler, priority=1.0)",  # Complete
            "StopAsyncIteration": "StopAsyncIterationHandler(ErrorSuggestHandler, priority=1.0)",  # Complete
            "ArithmeticError": {
                "ArithmeticError": "不设计。这个异常过于抽象，基本没人会单独抛",
                "FloatingPointError": "不设计。这个异常应当不再出现。",
                "OverflowError": "OverflowErrorHandler(ErrorSuggestHandler, priority=1.0)",  # Complete
                "ZeroDivisionError": "ZeroDivisionErrorHandler(ErrorSuggestHandler, priority=1.0)",  # Complete
            },
            "AssertionError": "AssertionErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
            "AttributeError": "AttributeErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
            "BufferError": "过于过于罕见了，能碰见的基本都是在玩底层的人，没必要给他们讲解，不设计",
            "EOFError": "EOFErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
            "ImportError": {
                "ImportError": "ImportErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
                "ModuleNotFoundError": "ModuleNotFoundErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
            },
            "LookupError": {
                "LookupError": "不设计。这个异常过于抽象，基本没人会单独抛",
                "IndexError": "IndexErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
                "KeyError": "KeyErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
            },
            "MemoryError": "MemoryErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
            "NameError": {
                "NameError": "NameErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
                "UnboundLocalError": "UnboundLocalErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
            },
            "OSError": {
                "OSError": "OSErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
                # 这个类别只设计几个常见的，太少见的就不设计了
                "BlockingIOError": "",
                "ChildProcessError": "",
                "ConnectionError": {
                    "ConnectionError": "",
                    "BrokenPipeError": "",
                    "ConnectionAbortedError": "",
                    "ConnectionRefusedError": "",
                    "ConnectionResetError": "",
                },
                "FileExistsError": "FileExistsErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
                "FileNotFoundError": "FileNotFoundErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
                "InterruptedError": "",
                "IsADirectoryError": "IsADirectoryErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
                "NotADirectoryError": "NotADirectoryErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
                "PermissionError": "PermissionErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
                "ProcessLookupError": "",
                "TimeoutError": "",
            },
            "ReferenceError": "实在过于罕见，疑似cpy完备化接口产物，不设计",
            "RuntimeError": {
                "RuntimeError": "RuntimeErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
                "NotImplementedError": "NotImplementedErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
                "RecursionError": "RecursionErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
            },
            "SyntaxError": {
                "SyntaxError": "SyntaxErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
                "IndentationError": {
                    "IndentationError": "IndentationErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
                    "TabError": "TabErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
                },
            },
            "SystemError": "SystemErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
            "TypeError": "TypeErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
            "ValueError": {
                "ValueError": "ValueErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
                "UnicodeError": {
                    "UnicodeError": "UnicodeErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
                    "UnicodeDecodeError": "UnicodeDecodeErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
                    "UnicodeEncodeError": "UnicodeEncodeErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
                    "UnicodeTranslateError": "UnicodeTranslateErrorHandler(ErrorSuggestHandler, priority=1.0)",  # TODO
                },
            }
        }
    }
}