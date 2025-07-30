"""
This module incorporates functions adapted from the Python standard
library's traceback module, with modifications made to certain function
signatures. Due to significant variations in traceback.py across
different Python versions, it provides stable Python implementation
interfaces for consistent functionality implementation.

The source code references CPython 3.12.8 and adheres to the following
licensing terms:

Copyright (c) 2001-2024 Python Software Foundation.
All Rights Reserved.

Copyright (c) 2000 BeOpen.com.
All Rights Reserved.

Copyright (c) 1995-2001 Corporation for National Research Initiatives.
All Rights Reserved.

Copyright (c) 1991-1995 Stichting Mathematisch Centrum, Amsterdam.
All Rights Reserved.

Used under the PSF LICENSE AGREEMENT FOR PYTHON 3.12.8:
https://docs.python.org/3/license.html
"""
import itertools
import sys
import textwrap

__all__ = [
    "sentinel",
    "parse_value_tb",
    "walk_stack",
    "walk_tb",
    "walk_tb_with_full_positions",
    "get_code_position",
    "byte_offset_to_character_offset",
    "ExceptionPrintContext",
    "levenshtein_distance",
    "compute_suggestion_error",
    "substitution_cost",
    "display_width",
]


def walk_stack(f):
    """Walk a stack yielding the frame and line number for each frame.

    This will follow f.f_back from the given frame. If no frame is given, the
    current stack is used. Usually used with StackSummary.extract.
    """
    if f is None:
        f = sys._getframe().f_back.f_back.f_back.f_back
    while f is not None:
        yield f, f.f_lineno
        f = f.f_back


def walk_tb(tb):
    """Walk a traceback yielding the frame and line number for each frame.

    This will follow tb.tb_next (and thus is in the opposite order to
    walk_stack). Usually used with StackSummary.extract.
    """
    while tb is not None:
        yield tb.tb_frame, tb.tb_lineno
        tb = tb.tb_next


def walk_tb_with_full_positions(tb):
    # Internal version of walk_tb that yields full code positions including
    # end line and column information.
    while tb is not None:
        positions = get_code_position(tb.tb_frame.f_code, tb.tb_lasti)
        # Yield tb_lineno when co_positions does not have a line number to
        # maintain behavior with walk_tb.
        if positions[0] is None:
            yield tb.tb_frame, (tb.tb_lineno,) + positions[1:]
        else:
            yield tb.tb_frame, positions
        tb = tb.tb_next


def get_code_position(code, instruction_index):
    if instruction_index < 0:
        return None, None, None, None
    positions_gen = code.co_positions()
    return next(itertools.islice(positions_gen, instruction_index // 2, None))


def byte_offset_to_character_offset(str_, offset):
    as_utf8 = str_.encode('utf-8')
    return len(as_utf8[:offset].decode("utf-8", errors="replace"))


_WIDE_CHAR_SPECIFIERS = "WF"


def display_width(line, offset):
    """Calculate the extra amount of width space the given source
    code segment might take if it were to be displayed on a fixed
    width output device. Supports wide unicode characters and emojis."""

    # Fast track for ASCII-only strings
    if line.isascii():
        return offset

    import unicodedata

    return sum(
        2 if unicodedata.east_asian_width(char) in _WIDE_CHAR_SPECIFIERS else 1
        for char in line[:offset]
    )


class ExceptionPrintContext:
    def __init__(self):
        self.seen = set()
        self.exception_group_depth = 0
        self.need_close = False

    def indent(self):
        return ' ' * (2 * self.exception_group_depth)

    def emit(self, text_gen, margin_char=None):
        if margin_char is None:
            margin_char = '|'
        indent_str = self.indent()
        if self.exception_group_depth:
            indent_str += margin_char + ' '

        if isinstance(text_gen, str):
            yield textwrap.indent(text_gen, indent_str, lambda line: True)
        else:
            for text in text_gen:
                yield textwrap.indent(text, indent_str, lambda line: True)


_MAX_CANDIDATE_ITEMS = 750
_MAX_STRING_SIZE = 40
_MOVE_COST = 2
_CASE_COST = 1


def substitution_cost(ch_a, ch_b):
    if ch_a == ch_b:
        return 0
    if ch_a.lower() == ch_b.lower():
        return _CASE_COST
    return _MOVE_COST


def compute_suggestion_error(exc_value, tb, wrong_name):
    if wrong_name is None or not isinstance(wrong_name, str):
        return None
    if isinstance(exc_value, AttributeError):
        obj = exc_value.obj
        try:
            d = dir(obj)
        except Exception:
            return None
    elif isinstance(exc_value, ImportError):
        try:
            mod = __import__(exc_value.name)
            d = dir(mod)
        except Exception:
            return None
    else:
        assert isinstance(exc_value, NameError)
        # find most recent frame
        if tb is None:
            return None
        while tb.tb_next is not None:
            tb = tb.tb_next
        frame = tb.tb_frame
        d = (
                list(frame.f_locals)
                + list(frame.f_globals)
                + list(frame.f_builtins)
        )

        # Check first if we are in a method and the instance
        # has the wrong name as attribute
        if 'self' in frame.f_locals:
            self = frame.f_locals['self']
            if hasattr(self, wrong_name):
                return f"self.{wrong_name}"

    # Compute closest match

    if len(d) > _MAX_CANDIDATE_ITEMS:
        return None
    wrong_name_len = len(wrong_name)
    if wrong_name_len > _MAX_STRING_SIZE:
        return None
    best_distance = wrong_name_len
    suggestion = None
    for possible_name in d:
        if possible_name == wrong_name:
            # A missing attribute is "found". Don't suggest it (see GH-88821).
            continue
        # No more than 1/3 of the involved characters should need changed.
        max_distance = (len(possible_name) + wrong_name_len + 3) * _MOVE_COST // 6
        # Don't take matches we've already beaten.
        max_distance = min(max_distance, best_distance - 1)
        current_distance = levenshtein_distance(wrong_name, possible_name, max_distance)
        if current_distance > max_distance:
            continue
        if not suggestion or current_distance < best_distance:
            suggestion = possible_name
            best_distance = current_distance
    return suggestion


def levenshtein_distance(a, b, max_cost):
    # A Python implementation of Python/suggestions.c:levenshtein_distance.

    # Both strings are the same
    if a == b:
        return 0

    # Trim away common affixes
    pre = 0
    while a[pre:] and b[pre:] and a[pre] == b[pre]:
        pre += 1
    a = a[pre:]
    b = b[pre:]
    post = 0
    while a[:post or None] and b[:post or None] and a[post - 1] == b[post - 1]:
        post -= 1
    a = a[:post or None]
    b = b[:post or None]
    if not a or not b:
        return _MOVE_COST * (len(a) + len(b))
    if len(a) > _MAX_STRING_SIZE or len(b) > _MAX_STRING_SIZE:
        return max_cost + 1

    # Prefer shorter buffer
    if len(b) < len(a):
        a, b = b, a

    # Quick fail when a match is impossible
    if (len(b) - len(a)) * _MOVE_COST > max_cost:
        return max_cost + 1

    # Instead of producing the whole traditional len(a)-by-len(b)
    # matrix, we can update just one row in place.
    # Initialize the buffer row
    row = list(range(_MOVE_COST, _MOVE_COST * (len(a) + 1), _MOVE_COST))

    result = 0
    for bindex in range(len(b)):
        bchar = b[bindex]
        distance = result = bindex * _MOVE_COST
        minimum = sys.maxsize
        for index in range(len(a)):
            # 1) Previous distance in this row is cost(b[:b_index], a[:index])
            substitute = distance + substitution_cost(bchar, a[index])
            # 2) cost(b[:b_index], a[:index+1]) from previous row
            distance = row[index]
            # 3) existing result is cost(b[:b_index+1], a[index])

            insert_delete = min(result, distance) + _MOVE_COST
            result = min(insert_delete, substitute)

            # cost(b[:b_index+1], a[:index+1])
            row[index] = result
            if result < minimum:
                minimum = result
        if minimum > max_cost:
            # Everything in this row is too big, so bail early.
            return max_cost + 1
    return result


class _Sentinel:
    def __repr__(self):
        return "<implicit>"


sentinel = _Sentinel()


def parse_value_tb(exc, value, tb):
    if (value is sentinel) != (tb is sentinel):
        raise ValueError("Both or neither of value and tb must be given")
    if value is tb is sentinel:
        if exc is not None:
            if isinstance(exc, BaseException):
                return exc, exc.__traceback__

            raise TypeError(f'Exception expected for value, '
                            f'{type(exc).__name__} found')
        else:
            return None, None
    return value, tb
