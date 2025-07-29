import os
from tdf_tool.modules.translate.flutter.flutter_tranalate_interface import (
    FlutterTranslateDartFileTool,
    FlutterTranslateToolsInterface,
)
from tdf_tool.modules.translate.tools.translate_tool import (
    MULTI_CODE_KEY,
    MULTI_MAF_KEY,
    MULTI_MIF_KEY,
)
from tdf_tool.tools.print import Print
from tdf_tool.tools.shell_dir import ShellDir
from tdf_tool.modules.multi_code.tools.serve_file import (
    GitlabServeFileTool,
    MultiCodeServerKeyDecs,
)


class FlutterMultiCodeTools(FlutterTranslateToolsInterface):
    """flutter MultiCode生成工具"""

    def translate_module(self, name, always_yes=False):
        businessModuleList = self.businessModuleList()
        if name in businessModuleList:
            Print.title(name + " 模块国际化脚本开始执行")
            self.__generateMultiCode(name)
            Print.title(name + " 模块国际化执行完成，生成 MultiCode")
        else:
            Print.error(name + " 模块不在开发列表中")

    def integrate(self):
        pass

    def clear_i18n_files(self):
        pass

    def __generateMultiCode(self, targetModule):
        ShellDir.goInModuleLibDir(targetModule)
        # 文本相关变量
        text_last_key = GitlabServeFileTool.read_text_last_key()
        i18n_text_dart_path = "tdf_intl/i18n.dart"
        text_decs: list[MultiCodeServerKeyDecs] = []

        # 图片资源相关变量
        res_last_key = GitlabServeFileTool.read_res_last_key()
        i18n_res_dart_path = "tdf_res_intl/res_i18n.dart"
        res_decs: list[MultiCodeServerKeyDecs] = []

        if not os.path.exists(i18n_text_dart_path):
            Print.error(i18n_text_dart_path + " 文件不存在")
        if not os.path.exists(i18n_res_dart_path):
            Print.error(i18n_res_dart_path + " 文件不存在")
        # 获取文案
        i18n_text_dict: dict[str, str] = (
            FlutterTranslateDartFileTool.getDartFileParamsJson(
                i18n_text_dart_path, MULTI_CODE_KEY
            )
        )
        for key, value in i18n_text_dict.items():
            if not value.startswith(MULTI_MAF_KEY):
                text_last_key += 1
                i18n_text_dict[key] = (
                    f"{MULTI_MAF_KEY}{GitlabServeFileTool.convert(text_last_key)}"
                )
            text_decs.append(
                MultiCodeServerKeyDecs(i18n_text_dict[key], targetModule, key)
            )

        # 更新server text相关文件
        GitlabServeFileTool.update_text_last_key(text_last_key)
        GitlabServeFileTool.update_text_decs(text_decs)
        # 更新i18n.dart文件
        i18n_text_dict_str = FlutterTranslateDartFileTool.generateDartMapFile(
            MULTI_CODE_KEY, i18n_text_dict
        )
        with open(i18n_text_dart_path, "w", encoding="utf-8") as f:
            f.write(i18n_text_dict_str)
            f.close()

        # 获取图片资源没有code的键集合
        i18n_res_dict = FlutterTranslateDartFileTool.getDartFileParamsJson(
            i18n_res_dart_path, MULTI_CODE_KEY
        )
        for key, value in i18n_res_dict.items():
            if not value.startswith(MULTI_MIF_KEY):
                res_last_key += 1
                i18n_res_dict[key] = (
                    f"{MULTI_MIF_KEY}{GitlabServeFileTool.convert(res_last_key)}"
                )
            res_decs.append(
                MultiCodeServerKeyDecs(i18n_res_dict[key], targetModule, key)
            )
        # 更新server res相关文件
        GitlabServeFileTool.update_res_last_key(res_last_key)
        GitlabServeFileTool.update_res_decs(res_decs)
        # 更新res_i18n.dart文件
        i18n_res_dict_str = FlutterTranslateDartFileTool.generateDartMapFile(
            MULTI_CODE_KEY, i18n_res_dict
        )
        with open(i18n_res_dart_path, "w", encoding="utf-8") as f:
            f.write(i18n_res_dict_str)
            f.close()
