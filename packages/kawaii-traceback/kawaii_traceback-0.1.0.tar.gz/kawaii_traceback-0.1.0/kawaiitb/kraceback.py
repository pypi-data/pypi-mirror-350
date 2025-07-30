"""
本文件重写了traceback中的部分结构，使其支持自定义的异常处理器。
结构与traceback.py相比有减改而无增。

"Extract, format and print information about Python stack traces."
"""

import collections.abc
import itertools
import linecache
import os
import sys
from contextlib import suppress
from dataclasses import dataclass
from typing import Optional, Type, TYPE_CHECKING, Generator

from kawaiitb.runtimeconfig import rc
from kawaiitb.utils import sys_getframe, extract_caret_anchors_from_line_segment, safe_string
from kawaiitb.utils.fromtraceback import (
    sentinel, parse_value_tb, walk_tb_with_full_positions,
    byte_offset_to_character_offset, walk_stack,
    ExceptionPrintContext, display_width,
)

if TYPE_CHECKING:
    from kawaiitb.kwihandler import ErrorSuggestHandler


class _ENV:
    def __init__(self):
        self.update()

    def update(self):
        """更新环境信息"""
        self.cwd = os.getcwd()
        self.platform = sys.platform

    def __getattr__(self, name):
        """按需获取新属性时自动更新"""
        self.update()
        return super().__getattribute__(name)

ENV = _ENV()


#
# 格式化和打印回溯信息
#

def print_list(extracted_list, file=None):
    """Print the list of tuples as returned by extract_tb() or
    extract_stack() as a formatted stack trace to the given file."""
    if file is None:
        file = sys.stderr
    for item in StackSummary.from_list(extracted_list).format():
        print(item, file=file, end="")


def format_list(extracted_list):
    """Format a list of tuples or FrameSummary objects for printing.

    Given a list of tuples or FrameSummary objects as returned by
    extract_tb() or extract_stack(), return a list of strings ready
    for printing.

    Each string in the resulting list corresponds to the item with the
    same index in the argument list.  Each string ends in a newline;
    the strings may contain internal newlines as well, for those items
    whose source text line is not None.
    """
    return StackSummary.from_list(extracted_list).format()


#
# 打印和提取异常
#

def print_tb(tb, limit=None, file=None):
    """Print up to 'limit' stack trace entries from the traceback 'tb'.

    If 'limit' is omitted or None, all entries are printed.  If 'file'
    is omitted or None, the output goes to sys.stderr; otherwise
    'file' should be an open file or file-like object with a write()
    method.
    """
    print_list(extract_tb(tb, limit=limit), file=file)


def format_tb(tb, limit=None):
    """A shorthand for 'format_list(extract_tb(tb, limit))'."""
    return extract_tb(tb, limit=limit).format()


def extract_tb(tb, limit=None):
    """
    Return a StackSummary object representing a list of
    pre-processed entries from traceback.

    This is useful for alternate formatting of stack traces.  If
    'limit' is omitted or None, all entries are extracted.  A
    pre-processed stack trace entry is a FrameSummary object
    containing attributes filename, lineno, name, and line
    representing the information that is usually printed for a stack
    trace.  The line is a string with leading and trailing
    whitespace stripped; if the source is not available it is None.
    """
    return StackSummary.extract_from_extended_frame_gen(
        walk_tb_with_full_positions(tb), limit=limit)


#
# 异常格式化与输出
#


def print_exception(exc, /, value=sentinel, tb=sentinel, limit=None, file=None, chain=True):
    """Print exception up to 'limit' stack trace entries from 'tb' to 'file'.

    This differs from print_tb() in the following ways: (1) if
    traceback is not None, it prints a header "Traceback (most recent
    call last):"; (2) it prints the exception type and value after the
    stack trace; (3) if type is SyntaxError and value has the
    appropriate format, it prints the line where the syntax error
    occurred with a caret on the next line indicating the approximate
    position of the error.
    """
    value, tb = parse_value_tb(exc, value, tb)
    te = KTBException(type(value), value, tb, limit=limit, compact=True)
    te.print(file=file, chain=chain)


def format_exception(exc, /, value=sentinel, tb=sentinel, limit=None, chain=True):
    """Format a stack trace and the exception information.

    The arguments have the same meaning as the corresponding arguments
    to print_exception().  The return value is a list of strings, each
    ending in a newline and some containing internal newlines.  When
    these lines are concatenated and printed, exactly the same text is
    printed as does print_exception().
    """
    value, tb = parse_value_tb(exc, value, tb)
    te = KTBException(type(value), value, tb, limit=limit, compact=True)
    return list(te.format(chain=chain))


def format_exception_only(exc, /, value=sentinel):
    """Format the exception part of a traceback.

    The return value is a list of strings, each ending in a newline.

    The list contains the exception's message, which is
    normally a single string; however, for :exc:`SyntaxError` exceptions, it
    contains several lines that (when printed) display detailed information
    about where the syntax error occurred. Following the message, the list
    contains the exception's ``__notes__``.
    """
    if value is sentinel:
        value = exc
    te = KTBException(type(value), value, None, compact=True)
    return list(te.format_exception_only())


# --

def print_exc(limit=None, file=None, chain=True):
    """Shorthand for 'print_exception(sys.exception(), limit, file, chain)'."""
    print_exception(sys.exception(), limit=limit, file=file, chain=chain)


def format_exc(limit=None, chain=True):
    """Like print_exc() but return a string."""
    return "".join(format_exception(sys.exception(), limit=limit, chain=chain))


def print_last(limit=None, file=None, chain=True):
    """This is a shorthand for 'print_exception(sys.last_exc, limit, file, chain)'."""
    if not hasattr(sys, "last_exc") and not hasattr(sys, "last_type"):
        raise ValueError("no last exception")

    if hasattr(sys, "last_exc"):
        print_exception(sys.last_exc, limit, file, chain)
    else:
        print_exception(sys.last_type, sys.last_value, sys.last_traceback,
                        limit, file, chain)


#
# 堆栈打印与提取
#

def print_stack(f=None, limit=None, file=None):
    """从调用点打印堆栈跟踪信息。

    可选参数'f'可指定起始堆栈帧，'limit'和'file'参数
    与print_exception()具有相同含义。
    """
    if f is None:
        f = sys_getframe().f_back
    print_list(extract_stack(f, limit=limit), file=file)


def format_stack(f=None, limit=None):
    """'format_list(extract_stack(f, limit))'的快捷方式"""
    if f is None:
        f = sys_getframe().f_back
    return format_list(extract_stack(f, limit=limit))


def extract_stack(f=None, limit=None):
    """从当前堆栈帧提取原始回溯信息。

    返回值格式与extract_tb()相同。可选参数'f'和'limit'
    与print_stack()含义相同。返回列表中的每个元素是四元组
    (文件名, 行号, 函数名, 代码文本)，按从最旧到最新
    堆栈帧的顺序排列。
    """
    if f is None:
        f = sys_getframe().f_back
    stack = StackSummary.extract(walk_stack(f), limit=limit)
    stack.reverse()
    return stack


def clear_frames(tb):
    """清除回溯中所有帧对局部变量的引用。"""
    while tb is not None:
        try:
            tb.tb_frame.clear()
        except RuntimeError:
            # 忽略帧仍在执行时抛出的异常
            pass
        tb = tb.tb_next


@dataclass
class FrameSummary:
    """表示回溯中单个帧的信息。

    - :attr:`filename` 该帧对应的文件名
    - :attr:`lineno` 捕获该帧时在文件中活跃的代码行号
    - :attr:`name` 捕获该帧时正在执行的函数或方法名称
    - :attr:`line` 来自linecache模块的该帧执行时的源代码文本
    - :attr:`locals_` 如果没有提供则为None，否则是变量名到其repr()表示的字典
    """

    __slots__ = ('filename', 'lineno', 'end_lineno', 'colno', 'end_colno',
                 'name', '_line', 'locals_')

    filename: str
    lineno: int
    name: str
    end_lineno: Optional[int]
    colno: Optional[int]
    end_colno: Optional[int]
    _line: Optional[str]
    locals_: Optional[dict]

    def __init__(self, filename, lineno, name, *, lookup_line=True,
                 locals_=None, line=None,
                 end_lineno=None, colno=None, end_colno=None):
        """构造FrameSummary对象。

        :param lookup_line: 如果为True，会立即通过linecache查找源代码行。
            否则推迟到首次需要时再查找
        :param locals_: 如果提供，会捕获帧的局部变量作为对象表示
        :param line: 如果提供，直接使用该行文本而不通过linecache查找
        """
        self.filename = filename
        self.lineno = lineno
        self.name = name
        self._line = line
        if lookup_line:  # 立即获取源代码行
            self.load_line()
        self.locals_ = {k: safe_string(v, 'local', func=repr)
                        for k, v in locals_.items()} if locals_ else None
        self.end_lineno = end_lineno
        self.colno = colno
        self.end_colno = end_colno

    def __eq__(self, other):
        if isinstance(other, FrameSummary):
            return (self.filename == other.filename and
                    self.lineno == other.lineno and
                    self.name == other.name and
                    self.locals_ == other.locals_)
        if isinstance(other, tuple):
            return (self.filename, self.lineno, self.name, self.line) == other
        return NotImplemented

    def __getitem__(self, pos):
        return (self.filename, self.lineno, self.name, self.line)[pos]

    def __iter__(self):
        return iter([self.filename, self.lineno, self.name, self.line])

    def __repr__(self):
        return "<FrameSummary file {filename}, line {lineno} in {name}>".format(
            filename=self.filename, lineno=self.lineno, name=self.name)

    def __len__(self):
        return 4

    @property
    def original_line(self):
        # 返回源代码中的原始行文本，不strip
        self.load_line()
        return self._line

    def load_line(self):
        if self._line is None:
            if self.lineno is None:
                return None
            self._line = linecache.getline(self.filename, self.lineno)
        return self._line.strip()

    @property
    def line(self):
        return self.load_line()


import os
import sysconfig
from pathlib import Path

def parse_module_filename(filename: str) -> str:
    """处理模块文件名，返回格式化后的显示字符串（跨平台优化版）"""
    # 优先处理标准库路径
    stdlib_path = Path(sysconfig.get_path("stdlib")).resolve()
    try:
        abs_path = Path(filename).resolve().relative_to(stdlib_path)
        parts = abs_path.parts
        if parts:
            return rc.translate(
                "config.file.parsed_filename",
                namespace=parts[0],
                filename=os.sep.join(parts)
            )
    except ValueError:
        pass

    # 工作区文件处理
    cwd = Path(ENV.cwd).resolve()
    try:
        rel_path = Path(filename).resolve().relative_to(cwd)
        if not rc.translate("config.file.include_cwd"):
            return str(rel_path)
        return filename
    except ValueError:
        pass

    # 第三方包路径检测
    normalized = os.path.normpath(filename).replace("\\", "/").lower()
    patterns = [
        ("site-packages", 1),  # 匹配层级
        ("dist-packages", 1),
        ("lib/python", 2),     # 跳过版本号目录
        ("lib64/python", 2),
        ("/python", 2),       # Windows 路径如 C:/Python312/Lib/
    ]

    for pattern, skip in patterns:
        index = normalized.find(f"/{pattern}/")
        if index != -1:
            parts = normalized[index+1:].split("/")[skip+1:]
            if parts:
                return rc.translate(
                    "config.file.parsed_filename",
                    namespace=parts[0],
                    filename=os.sep.join(parts)
                )

    return filename


# _RECURSIVE_CUTOFF = 3  # Also hardcoded in traceback.c.


class StackSummary(list[FrameSummary]):
    """FrameSummary对象的list, 表示异常帧的栈"""

    @classmethod
    def extract(cls, frame_gen, *, limit=None, lookup_lines=True,
                capture_locals=False):
        """从回溯或堆栈对象创建StackSummary。

        :param frame_gen: 生成(frame, lineno)元组的生成器，这些元组的摘要将被包含在堆栈中。
        :param limit: None表示包含所有帧，或指定要包含的帧数。
        :param lookup_lines: 如果为True，立即查找每个帧的源代码行，否则推迟到帧被渲染时再查找。
        :param capture_locals: 如果为True，将捕获每个帧的局部变量。作为对象表示到FrameSummary中。
        """

        def extended_frame_gen():
            for f, lineno in frame_gen:
                yield f, (lineno, None, None, None)

        return cls.extract_from_extended_frame_gen(
            extended_frame_gen(), limit=limit, lookup_lines=lookup_lines,
            capture_locals=capture_locals)

    @classmethod
    def extract_from_extended_frame_gen(cls, frame_gen, *, limit=None,
                                        lookup_lines=True, capture_locals=False):
        """从扩展的帧生成器提取堆栈信息

        参数:
        - frame_gen: 生成器，生成(frame, (lineno, end_lineno, colno, end_colno))格式的元组
        - limit: 限制提取的帧数量，None表示无限制
        - lookup_lines: 是否立即查找源代码行
        - capture_locals: 是否捕获局部变量

        返回:
        - StackSummary对象，包含提取的帧信息
        """

        # 处理最大深度限制
        if limit is None:
            # 从系统获取默认的traceback限制
            limit = getattr(sys, 'tracebacklimit', None)
            if limit is not None and limit < 0:
                # 如果限制为负数，则设为0
                limit = 0

        if limit is not None:
            if limit >= 0:
                # 正数限制：使用itertools.islice截取前limit个帧
                frame_gen = itertools.islice(frame_gen, limit)
            else:
                # 负数限制：使用collections.deque保留最后limit个帧
                frame_gen = collections.deque(frame_gen, maxlen=-limit)

        result = cls()  # 创建结果对象
        fnames = set()  # 用于存储所有文件名，避免重复加载

        # 遍历frame_gen，构建FrameSummary对象
        for f, (lineno, end_lineno, colno, end_colno) in frame_gen:
            co = f.f_code  # 获取代码对象

            filename = co.co_filename  # 获取文件名
            fnames.add(filename)  # 添加文件名到集合中

            name = co.co_name  # 获取函数名

            linecache.lazycache(filename, f.f_globals)  # 延迟加载文件内容到linecache

            # 是否捕获局部变量
            if capture_locals:
                f_locals = f.f_locals
            else:
                f_locals = None

            # 创建FrameSummary对象并添加到结果中
            result.append(FrameSummary(
                filename, lineno, name, lookup_line=False, locals_=f_locals,
                end_lineno=end_lineno, colno=colno, end_colno=end_colno))

        # 检查并更新linecache中的文件内容
        for filename in fnames:
            linecache.checkcache(filename)

        # 如果需要立即查找，现在触发查找
        if lookup_lines:
            for f in result:
                f.load_line()  # 加载源代码行, 放入了FrameSummary的_line

        return result

    @classmethod
    def from_list(cls, a_list):
        """
        从提供的FrameSummary对象列表或旧式元组列表创建StackSummary对象。
        """
        # 虽然进行isinstance(a_list, StackSummary)的快速检查很诱人，
        # 但idlelib.run.cleanup_traceback和其他类似代码可能会通过将任意帧
        # 转换为普通元组来破坏这一点，因此我们需要逐帧检查。
        result = StackSummary()
        for frame in a_list:
            if isinstance(frame, FrameSummary):
                result.append(frame)
            else:
                filename, lineno, name, line = frame
                result.append(FrameSummary(filename, lineno, name, line=line))
        return result

    def format_frame_summary(self, frame_summary: FrameSummary):
        """格式化单个FrameSummary的行。

        返回表示堆栈中单个帧的字符串。对于要打印在堆栈摘要中的每个帧，
        都会调用此方法。
        """
        # 文件名，据此判断是否为工作区，并判断是否包含工作区路径
        filename = parse_module_filename(frame_summary.filename)

        # 函数名，判断是否为模块级语句并翻译
        name = frame_summary.name
        if name == "<module>":
            name = rc.translate("config.module")
        elif name == "<string>":
            name = rc.translate("config.string")

        # 格式化帧信息行
        if frame_summary.colno is not None:
            row = [rc.translate('frame.location.with_column',
                                file=filename,
                                name=name,
                                lineno=frame_summary.lineno,
                                colno=frame_summary.colno)]
        else:
            row = [rc.translate('frame.location.without_column',
                                file=frame_summary.filename,
                                lineno=frame_summary.lineno,
                                name=frame_summary.name)]

        # 如果这个帧有可用的行文本
        if frame_summary.line:
            # 添加行文本到结果中
            stripped_line = frame_summary.line.strip()
            row.append(rc.translate('frame.location.linetext', line=stripped_line))

            # 如果有列位置信息，显示指示锚
            if (
                    frame_summary.colno is not None
                    and frame_summary.end_colno is not None
            ):
                # a = "s" + 1  语法上'"s" + 1'是错误产生的位置
                #     ~~~~^~~  而主字符"+"是错误产生的根本原因。

                # 处理问题帧的代码段基本内容
                line = frame_summary.original_line
                orig_line_len = len(line)
                frame_line_len = len(frame_summary.line.lstrip())
                stripped_characters = orig_line_len - frame_line_len
                start_offset = byte_offset_to_character_offset(line, frame_summary.colno)
                end_offset = byte_offset_to_character_offset(line, frame_summary.end_colno)
                code_segment = line[start_offset:end_offset]

                # 如果是单行问题帧, 语法树定位到引起错误的BinOp(+-*/等)或Subscript(a[b])操作
                offsets = None
                if frame_summary.lineno == frame_summary.end_lineno:
                    with suppress(Exception):
                        offsets = extract_caret_anchors_from_line_segment(code_segment)

                else:
                    # 不计算换行符，因为锚点只需定位到行的最后一个字符
                    end_offset = len(line.rstrip())

                # 如果主字符未跨越整行则添加定位锚行 ~~^~~
                if offsets and offsets[1] - offsets[0] > 0:
                    anchor_left, anchor_right = offsets

                    # 在终端显示时，某些非ASCII字符可能被渲染为双宽度字符，
                    # 因此在计算行长度时需要考虑这一点
                    dp_start_offset = display_width(line, start_offset) + 1
                    dp_left_end_offset = display_width(code_segment, anchor_left) + dp_start_offset
                    dp_right_start_offset = display_width(code_segment, anchor_right) + dp_start_offset
                    dp_end_offset = display_width(line, end_offset) + 1
                    anchor_indent = rc.translate("config.anchor.indent") + ' ' * (dp_start_offset - stripped_characters)
                    #  a =   1     /     0
                    # ....|~~~~~|^^^^^|~~~~~|
                    #   SO|  LEO|  RSO|   EO|
                    row.append(rc.anchors(
                        indent=anchor_indent,
                        left_start=dp_start_offset,
                        left_end=dp_left_end_offset,
                        right_start=dp_right_start_offset,
                        right_end=dp_end_offset,
                        crlf=True,
                    ))

                # 如果主字符未跨越整行则添加全指锚行 ^^^^^
                elif end_offset - start_offset < len(stripped_line):
                    dp_start_offset = display_width(line, start_offset) + 1
                    dp_end_offset = display_width(line, end_offset) + 1
                    anchor_indent = rc.translate("config.anchor.indent") + ' ' * (dp_start_offset - stripped_characters)
                    # what caaaaaan i say?
                    # ....|^^^^^^^^|
                    #   SO=LEO  RSO=EO
                    row.append(rc.anchors(
                        indent=anchor_indent,
                        left_start=dp_start_offset,
                        left_end=dp_start_offset,
                        right_start=dp_end_offset,
                        right_end=dp_end_offset,
                        crlf=True,
                    ))

        # 如果这个帧有携带的局部变量
        if frame_summary.locals_:
            # 逐个打印局部变量
            for name, value in sorted(frame_summary.locals_.items()):
                row.append(rc.translate('frame.location.locals_line', name=name, value=value))

        return ''.join(row)

    def format(self):
        """格式化堆栈信息以便打印。

        返回一个准备打印的字符串列表。结果列表中的每个字符串对应堆栈中的一个帧。
        每个字符串以换行符结尾；对于包含源代码文本行的项，字符串中可能也包含内部换行符。

        对于长时间重复的相同帧和行，会显示前几次重复，然后是一个总结行，说明确切的后续重复次数。
        """
        result = []
        last_file = None
        last_line = None
        last_name = None
        recursive_cutoff = rc.translate("config.stack.recursive_cutoff")
        if isinstance(recursive_cutoff, str) and recursive_cutoff.isdigit():
            recursive_cutoff = int(recursive_cutoff)
        if not isinstance(recursive_cutoff, int):
            import warnings
            warnings.warn(f"config.stack.recursive_cutoff must be an integer, but found ({type(recursive_cutoff)}){recursive_cutoff}, use default value {recursive_cutoff}")
            recursive_cutoff = 3

        count = 0
        for frame_summary in self:
            formatted_frame = self.format_frame_summary(frame_summary)
            if formatted_frame is None:
                continue

            # 重复组标记
            if (last_file is None or last_file != frame_summary.filename or
                    last_line is None or last_line != frame_summary.lineno or
                    last_name is None or last_name != frame_summary.name):  # 如果这是新的帧
                if count > recursive_cutoff:  # 且上一个帧重复了几次
                    count -= recursive_cutoff
                    result.append(rc.translate('config.stack.line_repeat_more', count=count))
                last_file = frame_summary.filename
                last_line = frame_summary.lineno
                last_name = frame_summary.name
                count = 0
            count += 1
            if count > recursive_cutoff:
                continue
            result.append(formatted_frame)

        if count > recursive_cutoff:
            count -= recursive_cutoff
            result.append(rc.translate('config.stack.line_repeat_more', count=count))
        return result



class KTBException:
    """
    一个准备好进行渲染的异常对象。

    回溯模块会从原始异常中捕获足够的属性到这个中间形式，以确保不保留任何引用，
    同时仍然能够完整地打印或格式化该异常。

    max_group_width 和 max_group_depth 控制异常组的格式化。
    深度指的是组的嵌套级别，
    宽度指的是单个异常组的异常数组的大小。
    当超过任一限制时，格式化输出将被截断。

    可以使用 `from_exception` 方法从异常对象创建 `TracebackException` 实例，
    也可以使用构造函数从单个组件创建 `TracebackException` 实例。

    - :attr:`__cause__` 原始异常 *__cause__* 对应的 `TracebackException` 实例。
    - :attr:`__context__` 原始异常 *__context__* 对应的 `TracebackException` 实例。
    - :attr:`exceptions` 对于异常组，这是一个包含嵌套 *exceptions* 对应的 `TracebackException` 实例的列表。对于其他异常，该值为 ``None``。
    - :attr:`__suppress_context__` 原始异常的 *__suppress_context__* 值。
    - :attr:`stack` 一个表示回溯信息的 `StackSummary` 对象。
    - :attr:`exc_type` 原始回溯的异常类。

    对于语法错误，还包含以下属性：
    - :attr:`filename` 语法错误发生的文件名。
    - :attr:`lineno` 语法错误发生的行号。
    - :attr:`end_lineno` 语法错误结束的行号。不存在时为 `None`。
    - :attr:`text` 语法错误发生处的文本。
    - :attr:`offset` 语法错误发生处文本的偏移量。
    - :attr:`end_offset` 语法错误结束处文本的偏移量。如果不存在，该值可以为 `None`。
    - :attr:`msg` 语法错误的编译器的错误消息。
    """
    _handler_types: list[Type["ErrorSuggestHandler"]] = []

    @classmethod
    def register(cls, Handler: Type["ErrorSuggestHandler"]):
        cls._handler_types.append(Handler)
        rc.register_handler(Handler)
        return Handler

    def __init__(self, exc_type, exc_value, exc_traceback, *, limit=None,
                 lookup_lines=True, capture_locals=False, compact=False,
                 max_group_width=15, max_group_depth=10, _seen=None):
        """
        初始化KTBException实例。

        参数:
        - exc_type: 异常类型
        - exc_value: 异常值
        - exc_traceback: 异常的回溯对象
        - limit: 限制回溯的深度
        - lookup_lines: 是否立即查找源代码行
        - capture_locals: 是否捕获局部变量
        - compact: 是否使用紧凑模式
        - max_group_width: 异常组的最大宽度
        - max_group_depth: 异常组的最大深度
        - _seen: 用于检测循环引用的已处理异常集合
        """


        # 处理 __cause__ 或 __context__ 中的循环。
        is_recursive_call = _seen is not None  # 是否是递归调用
        if _seen is None:
            _seen = set()
        _seen.add(id(exc_value))

        self.max_group_width = max_group_width
        self.max_group_depth = max_group_depth

        # 从回溯对象中提取堆栈信息
        self.stack: StackSummary = StackSummary.extract_from_extended_frame_gen(
            walk_tb_with_full_positions(exc_traceback),
            limit=limit, lookup_lines=lookup_lines,
            capture_locals=capture_locals)
        self.exc_type: Type[BaseException] = exc_type

        # 异常的字符串形式是它的原提示，比如"division by zero"
        # 或者'can only concatenate str (not "int") to str'
        self.exc_str = safe_string(exc_value, 'exception')

        # 获取异常的__notes__属性
        try:
            self.__notes__ = getattr(exc_value, '__notes__', None)
        except Exception as e:
            note_summary = safe_string(e, "__notes__", repr)
            self.__notes__ = [f'Ignored error getting __notes__: {note_summary}']

        self.final_exc_str = self.exc_str

        # 构建各个异常建议处理器便于后续提建议
        self._handlers: list["ErrorSuggestHandler"] = []
        for handler_type in self._handler_types:
            self._handlers.append(handler_type(exc_type, exc_value, exc_traceback, limit=limit,
                                               lookup_lines=lookup_lines, capture_locals=capture_locals,
                                               compact=compact, max_group_width=max_group_width,
                                               max_group_depth=max_group_depth, _seen=_seen))

        # 如果需要，加载源代码行
        if lookup_lines:
            self._load_lines()
        self.__suppress_context__ = \
            exc_value.__suppress_context__ if exc_value is not None else False

        # 使用队列处理__cause__和__context__，避免递归
        # 把所有的__cause__和__context__都挂到KTBException的__cause__, __context__, exceptions上, 完成引用解除
        self.exceptions: Optional[BaseExceptionGroup[BaseException]] = None
        if not is_recursive_call:  # 只允许首次创建的Kte创建处理队列，避免递归反复处理
            queue = [(self, exc_value)]
            while queue:
                te, e = queue.pop()
                # 处理cause
                if e and e.__cause__ is not None and id(e.__cause__) not in _seen:
                    cause = KTBException(
                        type(e.__cause__),
                        e.__cause__,
                        e.__cause__.__traceback__,
                        limit=limit,
                        lookup_lines=lookup_lines,
                        capture_locals=capture_locals,
                        max_group_width=max_group_width,
                        max_group_depth=max_group_depth,
                        _seen=_seen)
                else:
                    cause = None

                if compact:  # 紧凑模式下，只处理__suppress_context__为False的context
                    need_context = (cause is None and
                                    e is not None and
                                    not e.__suppress_context__)
                else:
                    need_context = True

                # 处理context
                if e and e.__context__ is not None and need_context and id(e.__context__) not in _seen:
                    context = KTBException(
                        type(e.__context__),
                        e.__context__,
                        e.__context__.__traceback__,
                        limit=limit,
                        lookup_lines=lookup_lines,
                        capture_locals=capture_locals,
                        max_group_width=max_group_width,
                        max_group_depth=max_group_depth,
                        _seen=_seen)
                else:
                    context = None

                # 处理异常组
                if e and isinstance(e, BaseExceptionGroup):
                    exceptions = []
                    for exc in e.exceptions:
                        texc = KTBException(
                            type(exc),
                            exc,
                            exc.__traceback__,
                            limit=limit,
                            lookup_lines=lookup_lines,
                            capture_locals=capture_locals,
                            max_group_width=max_group_width,
                            max_group_depth=max_group_depth,
                            _seen=_seen)
                        exceptions.append(texc)
                else:
                    exceptions = None

                te.__cause__ = cause
                te.__context__ = context
                te.exceptions = exceptions
                if cause:
                    queue.append((te.__cause__, e.__cause__))
                if context:
                    queue.append((te.__context__, e.__context__))
                if exceptions:
                    queue.extend(zip(te.exceptions, e.exceptions))

    @classmethod
    def from_exception(cls, exc, *args, **kwargs):
        """Create a TracebackException from an exception."""
        return cls(type(exc), exc, exc.__traceback__, *args, **kwargs)

    def _load_lines(self):
        """Private API. force all lines in the stack to be loaded."""
        for frame in self.stack:
            frame.load_line()

    def __eq__(self, other):
        if isinstance(other, KTBException):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __str__(self):
        return self.final_exc_str

    def format_exception_only(self):
        """格式化回溯中的异常部分。

        返回值是一个字符串Generator，每个字符串以换行符结尾。

        生成器会生成异常消息。

        对于 :exc:`SyntaxError` 异常，它还会在异常消息之前生成几行文本
        显示语法错误发生的详细位置信息。
        在异常消息之后，生成器还会生成该异常的所有 ``__notes__`` 属性内容。
        """
        if self.exc_type is None:
            if self.final_exc_str is None or not self.final_exc_str:
                yield rc.exc_line("UnknownError")
            else:
                yield rc.exc_line("UnknownError", self.final_exc_str)
            return

        stype: str = self.exc_type.__qualname__
        smod: str = self.exc_type.__module__
        if smod not in ("__main__", "builtins"):
            if not isinstance(smod, str):
                smod = "<unknown>"
            stype = smod + '.' + stype

        # 选择一个处理器，让它提提建议
        hi_priority = -1
        hi_priority_handler = None
        for handler in self._handlers:
            if handler.can_handle(self) and handler.priority > hi_priority:
                hi_priority = handler.priority
                hi_priority_handler = handler

        assert hi_priority_handler is not None, "No handler found for this exception. Why kwihandler.ErrorSuggestHandler not here?"
        yield from hi_priority_handler.handle(self)


        if (
            isinstance(self.__notes__, collections.abc.Sequence)
            and not isinstance(self.__notes__, (str, bytes))
        ):
            for note in self.__notes__:
                note = safe_string(note, 'note')
                yield from [l + '\n' for l in note.split('\n')]
        elif self.__notes__ is not None:
            yield "{}\n".format(safe_string(self.__notes__, '__notes__', func=repr))


    def format(self, *, chain =True, _ctx=None) -> Generator[str, None, None]:
        """格式化异常.

        如果 chain 不为 True，__cause__ 和 __context__ 不会递归地格式化。

        The return value is a generator of strings, each ending in a newline and
        some containing internal newlines. `print_exception` is a wrapper around
        this method which just prints the lines to a file.

        The message indicating which exception occurred is always the last
        string in the output.
        """

        if _ctx is None:
            _ctx = ExceptionPrintContext()

        output: list[tuple[Optional[str], Optional[KTBException]]] = []
        exc = self
        if chain:
            while exc:
                if exc.__cause__ is not None:
                    chained_msg = rc.translate("stack.cause")
                    chained_exc = exc.__cause__
                elif (exc.__context__ is not None and
                      not exc.__suppress_context__):
                    chained_msg = rc.translate("stack.context")
                    chained_exc = exc.__context__
                else:
                    chained_msg = None
                    chained_exc = None

                output.append((chained_msg, exc))
                exc = chained_exc
        else:
            output.append((None, exc))

        for msg, exc in reversed(output):
            if msg is not None:
                yield from _ctx.emit(msg)
            if exc.exceptions is None:
                if exc.stack:
                    yield from _ctx.emit(rc.translate("stack.summary"))
                    yield from _ctx.emit(exc.stack.format())
                yield from _ctx.emit(exc.format_exception_only())
            elif _ctx.exception_group_depth > self.max_group_depth:
                # 达到最大异常组深度，截断输出
                yield from _ctx.emit(
                    f"... (max_group_depth is {self.max_group_depth})\n")
            else:  # TODO: 这一整块是处理异常组的，但还没可翻译键值化，真烦人，异常组也没人用，以后再写
                # format exception group
                is_toplevel = (_ctx.exception_group_depth == 0)
                if is_toplevel:
                    _ctx.exception_group_depth += 1

                if exc.stack:
                    yield from _ctx.emit(
                        rc.translate("stack.group_summary"),
                        margin_char='+' if is_toplevel else None)
                    yield from _ctx.emit(exc.stack.format())

                yield from _ctx.emit(exc.format_exception_only())
                num_excs = len(exc.exceptions)
                if num_excs <= self.max_group_width:
                    n = num_excs
                else:
                    n = self.max_group_width + 1
                _ctx.need_close = False
                for i in range(n):
                    last_exc = (i == n - 1)
                    if last_exc:
                        # The closing frame may be added by a recursive call
                        _ctx.need_close = True

                    if self.max_group_width is not None:
                        truncated = (i >= self.max_group_width)
                    else:
                        truncated = False
                    title = f'{i + 1}' if not truncated else '...'
                    yield (_ctx.indent() +
                           ('+-' if i == 0 else '  ') +
                           f'+---------------- {title} ----------------\n')
                    _ctx.exception_group_depth += 1
                    if not truncated:
                        yield from exc.exceptions[i].format(chain=chain, _ctx=_ctx)
                    else:
                        remaining = num_excs - self.max_group_width
                        plural = 's' if remaining > 1 else ''
                        yield from _ctx.emit(
                            f"and {remaining} more exception{plural}\n")

                    if last_exc and _ctx.need_close:
                        yield (_ctx.indent() +
                               "+------------------------------------\n")
                        _ctx.need_close = False
                    _ctx.exception_group_depth -= 1

                if is_toplevel:
                    assert _ctx.exception_group_depth == 1
                    _ctx.exception_group_depth = 0

    def print(self, *, file=None, chain=True):
        """Print the result of self.format(chain=chain) to 'file'."""
        if file is None:
            file = sys.stderr
        for line in self.format(chain=chain):
            print(line, file=file, end="")
