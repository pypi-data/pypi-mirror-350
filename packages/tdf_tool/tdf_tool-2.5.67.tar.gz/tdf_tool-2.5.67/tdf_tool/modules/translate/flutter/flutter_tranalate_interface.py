# 国际化lint的接口
from abc import ABC, abstractmethod
import json

from tdf_tool.modules.config.initial_json_config import InitialJsonConfig
from tdf_tool.modules.config.module_json_config import ModuleJsonConfig, ModuleItemType
from tdf_tool.modules.translate.tools.translate_tool import LanguageType
from tdf_tool.tools.print import Print
from tdf_tool.tools.shell_dir import ShellDir
from tdf_tool.tools.env import EnvTool
from tdf_tool.modules.translate.tools.translate_enable import TranslateEnable


class FlutterTranslateDartFileTool:
    # 通过json生成dart.map
    def generateDartMapFile(var_name: str, paramsJson: dict) -> str:
        return r"Map<String, String> {0}Map = {1};".format(
            var_name,
            json.dumps(paramsJson, ensure_ascii=False, indent=2, sort_keys=True),
        )

    # 获取目标文件dart内json数据
    def getDartFileParamsJson(targetFileName, mapName) -> dict:
        with open(targetFileName, "r", encoding="utf-8") as readF:
            try:
                Print.str("解析{0}文件内json数据".format(targetFileName))
                fileData = readF.read()
                fileJsonData = FlutterTranslateDartFileTool.__correctJsonData(
                    fileData, mapName
                )
                jsonData = json.loads(fileJsonData, strict=False)
                readF.close()
                return jsonData
            except Exception as e:
                readF.close()
                return {}

    # 从map中返回正确的json字符串
    def __correctJsonData(content, mapName) -> str:
        return (
            str(content.replace("Map<String, String> {0}Map =".format(mapName), ""))
            .replace("\n", "")
            .strip(",};")
            .__add__("}")
        )


# 翻译Dart文件操作的实现
class FlutterTranslateDartFileMixin:

    # 通过json生成dart.map
    def generateDartMapFile(self, var_name: str, paramsJson: dict) -> str:
        return FlutterTranslateDartFileTool.generateDartMapFile(var_name, paramsJson)

    # 获取目标文件dart内json数据
    def getDartFileParamsJson(self, targetFileName, mapName) -> dict:
        return FlutterTranslateDartFileTool.getDartFileParamsJson(
            targetFileName, mapName
        )


class FlutterTranslateModuleTool:
    # 可以进行国际化的列表
    @staticmethod
    def businessModuleList() -> list:
        __initialConfig = InitialJsonConfig()
        __moduleConfig = ModuleJsonConfig()
        businessModuleList = []
        ShellDir.goInShellDir()
        for item in __initialConfig.moduleNameList:
            module_item = __moduleConfig.get_item(item)
            if (
                module_item.type == ModuleItemType.Module
                or module_item.type == ModuleItemType.Lib
                or module_item.type == ModuleItemType.Plugin
                or module_item.type == ModuleItemType.Api
                or module_item.type == ModuleItemType.Flutter
            ):
                gitlab_ci_path = (
                    ShellDir.workspace()
                    + "/../.tdf_flutter/"
                    + item
                    + "/.gitlab-ci.yml"
                )
                if TranslateEnable(gitlab_ci_path).no_translate:
                    continue
                businessModuleList.append(item)
        return businessModuleList

    # 传入的库是否可以进行国际化
    @staticmethod
    def can_translate(module_name: str) -> bool:
        __moduleConfig = ModuleJsonConfig()
        module_item = __moduleConfig.get_item(module_name)
        if (
            module_item.type == ModuleItemType.Module
            or module_item.type == ModuleItemType.Lib
            or module_item.type == ModuleItemType.Plugin
            or module_item.type == ModuleItemType.Api
            or module_item.type == ModuleItemType.Flutter
        ):
            gitlab_ci_path = (
                ShellDir.workspace()
                + "/../.tdf_flutter/"
                + module_name
                + "/.gitlab-ci.yml"
            )
            if TranslateEnable(gitlab_ci_path).no_translate:
                return False
        return True

    # 当前的lib路径是否可以国际化
    @staticmethod
    def can_translate_lib_path(lib_path: str) -> bool:
        gitlab_ci_path = lib_path + "/../.gitlab-ci.yml"
        if TranslateEnable(gitlab_ci_path).no_translate:
            return False
        return True

    @staticmethod
    def filter_file(file: str, root: str) -> bool:
        return (
            file.endswith(".dart")
            and not root.__contains__("/tdf_res_intl")
            and not root.__contains__("/tdf_intl")
            and not file.endswith(".tdf_router.dart")
        )


class FlutterTranslateModuleMixin:
    # 可以进行国际化的列表
    def businessModuleList(self) -> list:
        return FlutterTranslateModuleTool.businessModuleList()

    # 传入的库是否可以进行国际化
    def can_translate(self, module_name: str) -> bool:
        return FlutterTranslateModuleTool.can_translate(module_name)

    # 当前的lib路径是否可以国际化
    def can_translate_lib_path(self, lib_path: str) -> bool:
        return FlutterTranslateModuleTool.can_translate_lib_path(lib_path)

    def filter_file(self, file: str, root: str) -> bool:
        return FlutterTranslateModuleTool.filter_file(file, root)


# 国际化的接口
class FlutterTranslateToolsInterface(
    ABC, FlutterTranslateDartFileMixin, FlutterTranslateModuleMixin
):
    @abstractmethod
    def translate_module(self, name, always_yes=False):
        pass

    @abstractmethod
    def integrate(self):
        pass

    @abstractmethod
    def clear_i18n_files(self):
        pass

    def getManagerClassName(self, moduleName):
        strList = moduleName.split("_")
        result = ""
        for item in strList:
            result = result + item.capitalize()
        return result

    # 将i8n的dart文件转换为excel的dict
    def generateI18nExcelDict(self, path: str) -> dict:
        # 所有语言的翻译数据，key为中文，value为各个语言翻译后的数据list
        result_dict = {}
        # 遍历所有语言文件
        all_lang = LanguageType.all()
        for lang in all_lang:
            file_path = f"{path}_{lang.str()}.dart"
            # 拿到所有dart数据中的内容
            pairs = self.getDartFileParamsJson(file_path, lang.str())
            # 将数据添加到all_data_dict中
            for key, value in pairs.items():
                if key not in result_dict:
                    # 初始化一个空列表，长度为语言文件数量
                    result_dict[key] = [""] * len(all_lang)
                # 找到当前语言在列表中的索引
                lang_index = all_lang.index(lang)
                result_dict[key][lang_index] = value

        # 将result_dict.values()的行跟列互换
        result_list = list(zip(*result_dict.values()))
        # 生成excel文件
        excel_dict = {}
        for i, v in enumerate(result_list):
            excel_dict[all_lang[i].str()] = v
        return excel_dict
