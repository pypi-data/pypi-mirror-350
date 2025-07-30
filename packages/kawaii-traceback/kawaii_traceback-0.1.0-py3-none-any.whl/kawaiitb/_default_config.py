r"""
kawaii-traceback 多语言配置系统说明

===== 静态扩展翻译键 =====

语言配置是一个json文件或python字典，包含以下结构:
{
    "translate_keys": 翻译键值对
        "(your_lang)": 你的翻译名
            "extend": str;你要继承的翻译名  <== 如果没有，默认继承default
            "(some.keywords)": str;各种翻译键  <== 可翻译键值对可以在下面的default中找到
    "default_lang": str;默认语言  <== 如果希望你的翻译加载后能够立刻生效，在这个键中指定你的翻译名
}
注意：
- 翻译名应当是有效的python标识符 + "(要继承的翻译名)". 继承的翻译名可以省略其父继承
- 通过包含 extend 键指定父配置. 实际的继承关系以此键名决定. 未指定会自动继承default.
- 在python字典中使用EXTENDED显示指定一个翻译键的父翻译. 在json中使用"==EXTEND==".

===== 动态扩展翻译键 =====

你可以通过继承 kawaiitb.ErrorSuggestHandler来定义一个动态扩展的**提示信息**.
提示信息只在一部分动态生成。例如：

...... Traceback (most recent call last):
......   File "C:\Users\BPuffer\Desktop\kawaii-traceback\main.py", line 74:8, in <module>
......     asyncio.run(asyncio.sleep(1))
......     ^^^^^^^
HINT-> NameError: name 'asyncio' is not defined
HINT-> 猜你没导入: 'asyncio'

动态生成的灵活性很高，你除了可以获取异常本身外还能获得当前运行代码的上下文信息。比如使用本库还原的原生语法错误特殊解析：
...... Traceback (most recent call last):
......   File "C:\Users\BPuffer\Desktop\kawaii-traceback\main.py", line 138:8, in <module>
......     exec("what can i say?")
HINT->   File "<string>", line 1
HINT->     what can i say?
HINT->          ^^^
HINT-> SyntaxError: invalid syntax (<string>, line 1)

---

如果你希望使用动态扩展，参阅 kawaiitb.kwihandler.py 中的示例.
"""
__all__ = [
    "DEFAULT_CONFIG",
    "EXTENDED",
]

EXTENDED = "==EXTEND=="  # 标记继承父翻译项

DEFAULT_CONFIG = {
    "translate_keys": {
        "default": {
            # 交互式提示符
            "config.prompt1": ">>> ",
            "config.prompt2": "... ",

            # 重复的帧
            "config.stack.recursive_cutoff": 3,
            "config.stack.line_repeat_more": '  [Previous line repeated {count} more times]\n',

            # 文件路径解析
            "config.file.include_cwd": True,
            "config.file.parse_module_filename": False,
            "config.file.parsed_filename": "[{namespace}] {filename}",
            "config.module": "<module>",
            "config.string": "<string>",

            # 锚点
            "config.anchor.indent": ' ' * 4,
            "config.anchor.primary": '~',
            "config.anchor.secondary": '^',
            "config.anchor.suffix": '',

            # 单帧格式化
            "frame.location.with_column": '  File "{file}", line {lineno}:{colno}, in {name}\n',
            "frame.location.without_column": '  File "{file}", line {lineno}, in {name}\n',
            "frame.location.without_name": '  File "{file}", line {lineno}\n',
            "frame.location.linetext": '    {line}\n',
            "frame.location.locals_line": '    {name} = {value}\n',

            # 帧栈格式化
            "stack.cause": "\nThe above exception was the direct cause of the following exception:\n\n",
            "stack.context": "\nDuring handling of the above exception, another exception occurred:\n\n",
            "stack.summary": "Traceback (most recent call last):\n",
            "stack.group_summary": "Exception Group Traceback (most recent call last):\n",

            # 各个异常格式化
            "exception.message": "{etype}: {value}\n",
            "exception.exc_line_noval": "{etype}\n",
            "exception.exc_line": "{etype}: {value}\n",
            "exception.qualname": "{qualname}",
            "exception.module_qualname": "{module}.{qualname}",
            "exception.note": "{note}\n",
        },
        "en_us": {},  # 继承default
        "zh_hans": {  # 简体中文配置
            "config.file.include_cwd": False,
            "config.module": "模块级语句",
            "config.string": "注入的语句",
            "frame.location.with_column": '  文件 {file}:{lineno}:{colno} 的 {name}\n',
            "frame.location.without_column": '  文件 {file}:{lineno} 的 {name}\n',
            "frame.location.without_name": '  文件 "{file}:{lineno}"\n',
            "stack.cause": "\n该异常引发了另一个异常:\n\n",
            "stack.context": "\n处理上面的异常时，发生了如下异常:\n\n",
            "stack.summary": "异常回溯 (到最近一次调用):\n",
            "config.stack.line_repeat_more": ' (*在那之后, 这一行重复了 {count} 次)\n',
        },
        "neko_zh": {  # 萌化中文配置示例
            "extend": "zh_hans",
            "stack.summary": "pypy被玩坏了！这肯定不是py的问题！绝对不是！\n",
            "config.file.parse_module_filename": True,
            "config.file.parsed_filename": "[{namespace} 模块] {filename}",
            "config.prompt1": "owo!> ",
            "config.prompt2": "=w=~| ",
            "config.anchor.suffix": " ↖在这里喵~",

            "exception.message": "[{etype}] {value}\n",
            "exception.exc_line_noval": "[{etype}]!\n",
            "exception.exc_line": "[{etype}] {value}\n",
        },
        "kirakira": {  # 二次扩展示例
            "extend": "neko_zh",
            "stack.summary": "☆pypy被玩坏了☆这肯定不是py的问题☆绝对不是☆\n",
            "config.prompt1": "✧⋆˚｡~˚~｡> ",
            "config.prompt2": "✧ :*✧･ﾟ:| ",
        }
    },
    "default_lang": "neko_zh",
}

if __name__ == "__main__":
    # 示例自定义配置
    new_config = {
        "translate_keys": {
            "neko_zh": {
                "extend": "zh_hans",
                "config.file.parse_module_filename": True,
                "frame.location.with_column": EXTENDED,
                "config.anchor.suffix": " ↖在这里喵~",
            }
        },
        "default_lang": "neko_zh"
    }
    # 此处以字典格式为例。JSON配置可以使用`kawaiitb.load(open('your_config.json'))`
