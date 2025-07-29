import os

from tdf_tool.modules.translate.flutter.flutter_tranalate_interface import (
    FlutterTranslateDartFileTool,
)
from tdf_tool.modules.translate.flutter.flutter_translate_lint_interface import (
    FlutterTranslateLintInterface,
)
from tdf_tool.modules.translate.tools.translate_tool import (
    MULTI_CODE_KEY,
    MULTI_MAF_KEY,
    MULTI_MIF_KEY,
)
from tdf_tool.tools.print import Print
from tdf_tool.tools.shell_dir import ShellDir


class MultiCodeLintResult:
    def __init__(
        self,
        miss_text_codes: list[str],
        miss_res_codes: list[str],
    ):
        # 缺少文案code集合
        self.miss_text_codes = miss_text_codes
        # 缺少图片code集合
        self.miss_res_codes = miss_res_codes


class FlutterMultiCodeLint(FlutterTranslateLintInterface):
    """flutter 后台下发国际化规范工具"""

    def lint_all(self):
        """
        全部模块 lint
        """
        results = []
        pass_result = True
        for module in self.businessModuleList():
            result = FlutterMultiCodeLint.get_lint_module_result(module)
            results.append(result)
            if not FlutterMultiCodeLint.__lint_result(result):
                pass_result = False
                Print.error(module + " 模块国际化 lint 失败", shouldExit=False)
            else:
                Print.title(module + " 模块国际化 lint 成功")
        if pass_result:
            print("\n")
            Print.title("国际化 lint 通过")
        else:
            Print.error("国际化 lint 失败")

    def lint_module(self, name):
        """
        指定模块 lint
        """
        if not self.can_translate(name):
            Print.warning(name + " 模块不需要国际化")
            return
        result = FlutterMultiCodeLint.get_lint_module_result(name)
        if FlutterMultiCodeLint.__lint_result(result):
            Print.stage(name + " 模块国际化 lint 通过")
        else:
            Print.error(name + " 模块国际化 lint 失败")

    def lint_path(self, path):
        """
        指定模块路径 lint，路径为 lib 路径
        """
        if not self.can_translate_lib_path(path):
            Print.warning(path + " 不需要国际化")
            return
        result = FlutterMultiCodeLint.__lint_intl_path(path)
        if FlutterMultiCodeLint.__lint_result(result):
            Print.title(path + " 路径国际化 lint 通过")
        else:
            Print.error(path + " 路径国际化lint 失败")

    @staticmethod
    def get_lint_module_result(module_name: str) -> MultiCodeLintResult:
        print("\n")
        Print.title(module_name + " 模块国际化 lint 开始执行")
        target_path = ShellDir.getModuleLibDir(module_name)
        if os.path.exists(target_path):
            return FlutterMultiCodeLint.__lint_intl_path(target_path)
        else:
            Print.error(target_path + "路径不存在")

    @staticmethod
    def __lint_intl_path(path: str) -> MultiCodeLintResult:
        """检查 i18n.dart 文件是否缺少code"""
        Print.stage(f"{path}开始检查i18n.dart文件是否缺少code")
        i18n_text_dart_path = f"{path}/tdf_intl/i18n.dart"
        i18n_res_dart_path = f"{path}/tdf_res_intl/res_i18n.dart"
        if not os.path.exists(i18n_text_dart_path):
            Print.error(i18n_text_dart_path + " 文件不存在")
        if not os.path.exists(i18n_res_dart_path):
            Print.error(i18n_res_dart_path + " 文件不存在")
        # 获取文案没有code的键集合
        missing_text_keys: list[str] = []
        i18n_text_dict: dict[str, str] = (
            FlutterTranslateDartFileTool.getDartFileParamsJson(
                i18n_text_dart_path, MULTI_CODE_KEY
            )
        )
        for key, value in i18n_text_dict.items():
            if not value.startswith(MULTI_MAF_KEY):
                missing_text_keys.append(key)

        # 获取图片资源没有code的键集合
        missing_res_keys: list[str] = []
        i18n_res_dict = FlutterTranslateDartFileTool.getDartFileParamsJson(
            i18n_res_dart_path, MULTI_CODE_KEY
        )
        for key, value in i18n_res_dict.items():
            if not value.startswith(MULTI_MIF_KEY):
                missing_res_keys.append(key)

        return MultiCodeLintResult(missing_text_keys, missing_res_keys)

    # 校验 lint 的结果
    def __lint_result(result: MultiCodeLintResult) -> bool:
        # 检查miss_text_codes
        if len(result.miss_text_codes) > 0:
            Print.warning("以下文案缺少code：")
            Print.str(result.miss_text_codes)
        # 检查miss_res_codes
        if len(result.miss_res_codes) > 0:
            Print.warning("以下图片缺少code：")
            Print.str(result.miss_res_codes)

        return len(result.miss_res_codes) == 0 and len(result.miss_res_codes) == 0
