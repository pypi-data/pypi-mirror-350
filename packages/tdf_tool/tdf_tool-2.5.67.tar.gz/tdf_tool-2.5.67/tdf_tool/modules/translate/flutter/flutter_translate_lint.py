from tdf_tool.modules.multi_code.flutter.flutter_multi_code_lint import (
    FlutterMultiCodeLint,
)
from tdf_tool.modules.translate.flutter.flutter_translate_lint_interface import (
    FlutterTranslateLintInterface,
)
from tdf_tool.modules.translate.flutter.resource.flutter_res_translate_lint import (
    FlutterResTranslateLint,
)
from tdf_tool.modules.translate.flutter.text.flutter_text_translate_lint import (
    FlutterTextTranslateLint,
)
from tdf_tool.tools.print import Print


class FlutterTranslateLintFactory(FlutterTranslateLintInterface):

    def __init__(self):
        self._text_lint = FlutterTextTranslateLint()
        self._res_lint = FlutterResTranslateLint()
        self._i18n_lint = FlutterMultiCodeLint()

    def start(self, all_module=False):
        """
        以交互的方式选择需要 lint 的模块
        """
        businessModuleList = self.businessModuleList()
        Print.str("检测到以下模块可执行国际化lint：")
        Print.str(businessModuleList)
        inputStr = "!"
        if all_module:
            inputStr = "all"
        else:
            inputStr = input("请输入需要执行 lint 的模块名(input ! 退出, all 全选)：")

        if inputStr == "!" or inputStr == "！":
            exit(0)
        elif inputStr == "all":
            self.lint_all()
            exit(0)
        elif inputStr in businessModuleList:
            self.lint_module(inputStr)
            exit(0)

    def lint_all(self):
        """
        全量 lint
        """
        self._res_lint.lint_all()
        self._text_lint.lint_all()
        self._i18n_lint.lint_all()

    def lint_module(self, name):
        """
        指定模块 lint，路径为 lib 路径
        """
        self._res_lint.lint_module(name)
        self._text_lint.lint_module(name)
        self._i18n_lint.lint_module(name)

    def lint_path(self, path):
        """
        指定模块路径 lint，路径为 lib 路径
        """
        self._res_lint.lint_path(path)
        self._text_lint.lint_path(path)
        self._i18n_lint.lint_path(path)
