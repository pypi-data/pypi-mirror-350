import pytest

import kawaiitb
from test.utils.utils import KTBTestBase, setup_test


class TestExceptionFormatting(KTBTestBase, console_output=True):
    def test_recursive_exception(self):
        """测试递归异常深度溢出"""
        setup_test()
        try:
            f = lambda x: f(x + 1)
            f(1)
        except Exception as e:
            tb = "".join(kawaiitb.traceback.format_exception(e))
            self.try_print_exc(e)
            assert "*在那之后" in tb

    def test_exception_with_notes(self):
        """测试带__notes__的异常"""
        class CustomException(Exception):
            def __init__(self, *args):
                super().__init__(*args)
                self.__notes__ = ["note1", "note2"]

        try:
            raise CustomException("test")
        except Exception as e:
            tb = "".join(kawaiitb.traceback.format_exception(e))
            self.try_print_exc(e)
            assert "test.test_tb_format.TestExceptionFormatting.test_exception_with_notes.<locals>.CustomException" in tb
            assert "note1\nnote2" in tb

    def test_in_package_error(self):
        """测试项目中模块的异常"""
        try:
            from test.utils.utils import raise_error
            raise_error()
        except Exception as e:
            import os
            tb = "".join(kawaiitb.traceback.format_exception(e))
            self.try_print_exc(e)
            # 应当截断了项目路径
            assert r"C://" not in tb and r"C:\\" not in tb  # Windows
            assert "文件 " + os.sep not in tb  # Linux

    def test_lib_module_error(self):
        """测试标准库模块异常"""
        import os
        try:
            import asyncio
            async def f():
                await asyncio.sleep(0)
                raise Exception("test")

            asyncio.run(f())
        except Exception as e:
            tb = "".join(kawaiitb.traceback.format_exception(e))
            self.try_print_exc(e)
            assert "asyncio 模块" in tb  # 显示模块名
            # 截断到lib或者site-packages
            assert "asyncio" + os.sep in tb
            assert os.sep + "asyncio" not in tb

    @pytest.mark.skip(reason="TODO")
    def test_long_line_formatting(self):
        """测试超长行异常格式化"""
        try:
            raise Exception(
                "This is a very long exception message that should be properly formatted and wrapped when displayed in the traceback output.")
        except Exception as e:
            tb = "".join(kawaiitb.traceback.format_exception(e))
            self.try_print_exc(e)
            assert len(tb.splitlines()) > 1  # 检查是否自动换行

    @pytest.mark.skip(reason="非项目帧简化 TODO")
    def test_site_package_error(self):
        """测试隔着一大堆模块的异常"""
        import asyncio
        async def task():
            await asyncio.sleep(0)
            raise Exception("test")

        asyncio.run(task())