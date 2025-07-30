import kawaiitb
from .utils.utils import KTBTestBase


class TestAnchor(KTBTestBase, console_output=False):
    # 1. 语法错误测试
    def test_syntax_error_anchor_invalid_lex(self):
        """测试无效词法语法错误"""
        try:
            exec("what can i say?")  # noqa
        except SyntaxError as e:
            tb = "".join(kawaiitb.traceback.format_exception(e))
            self.try_print_exc(e)
            assert """
    what can i say?
         ^^^""" in tb

    def test_syntax_error_anchor_incomplete_expr(self):
        """测试不完整表达式语法错误"""
        try:
            exec("1 + 2 *")  # noqa
        except SyntaxError as e:
            tb = "".join(kawaiitb.traceback.format_exception(e))
            self.try_print_exc(e)
            assert """
    1 + 2 *
           ^""" in tb

    def test_type_error_anchor_binop(self):
        """测试二元操作类型错误锚"""
        try:
            _ = "s" + 1  # noqa
        except TypeError as e:
            tb = "".join(kawaiitb.traceback.format_exception(e))
            self.try_print_exc(e)
            assert """
    _ = "s" + 1  # noqa
        ~~~~^~~""" in tb

    def test_type_error_anchor_subscript(self):
        """测试取键类型错误锚"""
        try:
            d = {"a": 1}["b"]  # noqa
        except KeyError as e:
            tb = "".join(kawaiitb.traceback.format_exception(e))
            self.try_print_exc(e)
            assert """
    d = {"a": 1}["b"]  # noqa
        ~~~~~~~~^^^^^""" in tb

    def test_zero_division_anchor(self):
        """测试除零错误锚"""
        try:
            _ = 1 / 0  # noqa
        except ZeroDivisionError as e:
            tb = "".join(kawaiitb.traceback.format_exception(e))
            self.try_print_exc(e)
            assert """
    _ = 1 / 0  # noqa
        ~~^~~""" in tb

    def test_attribute_error_anchor(self):
        """测试属性错误锚"""
        class Person:
            def __init__(self, name, age):
                self.name = name
                self.age = age

        try:
            person = Person("Alice", 30)
            _ = person.nonexistent_attribute  # noqa
        except AttributeError as e:
            tb = "".join(kawaiitb.traceback.format_exception(e))
            self.try_print_exc(e)
            assert """
    _ = person.nonexistent_attribute  # noqa
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^""" in tb

