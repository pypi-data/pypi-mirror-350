import sys
from io import StringIO

import pytest

from test.utils.utils import KTBTestBase

custom_conf = """{
  "translate_keys": {
    "test_conf": {
      "stack.summary": "Test summary qwertyuiopasdfghjklzxcvbnm\\n"
    },
    "another_lang": {
      "stack.summary": "Test summary 1234567890\\n"
    }
  },
  "default_lang": "test_conf"
}"""  # "\\n" is necessary
test_conf = "Test summary qwertyuiopasdfghjklzxcvbnm"
another_lang = "Test summary 1234567890"
kirakira = "☆pypy被玩坏了☆这肯定不是py的问题☆绝对不是☆"


class TestKTBLoad(KTBTestBase, console_output=False):
    def test_module_load(self):
        def is_changed():
            return sys.excepthook != sys.__excepthook__

        assert not is_changed(), "默认的异常钩子未被正确加载"

        import kawaiitb
        assert not is_changed(), "import kawaiitb 时异常钩子被提前加载"

        kawaiitb.load()
        assert is_changed(), "kawaiitb.load() 未能正确加载异常钩子"

        kawaiitb.unload()
        assert not is_changed(), "kawaiitb.unload() 未能正确卸载异常钩子"

        import kawaiitb.autoload  # noqa
        assert is_changed(), "import kawaiitb.load 未能正确自动加载异常钩子"

    def get_exception_summary(self):
        from kawaiitb import kraceback
        with pytest.raises(ZeroDivisionError) as excinfo:
            _ = 1 / 0
        e = excinfo.value
        self.try_print_exc(e)
        return "".join(kraceback.format_exception(e))

    def test_load_defualt(self):
        from kawaiitb import load, unload
        load()
        assert "KawaiiTB" in self.get_exception_summary()
        unload()

    def test_load_lang(self):
        from kawaiitb import load, unload
        load('kirakira')
        assert kirakira in self.get_exception_summary()
        unload()

    def test_load_fileio(self):
        from kawaiitb import load, unload
        load(StringIO(custom_conf))
        assert test_conf in self.get_exception_summary()
        unload()

    def test_load_fileio_lang(self):
        from kawaiitb import load, unload
        load('another_lang', StringIO(custom_conf))
        assert another_lang in self.get_exception_summary()
        unload()
        assert sys.excepthook == sys.__excepthook__, "kawaiitb.unload() 未能正确卸载异常钩子"
