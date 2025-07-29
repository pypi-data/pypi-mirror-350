import json
import os
import concurrent.futures
from tdf_tool.modules.multi_code.tools.serve_file import GitlabServeFileTool
from tdf_tool.tools.platform_tools import PlatformTools
from tdf_tool.modules.translate.flutter.flutter_translate_tools import (
    FlutterTranslateToolsInterface,
)
from tdf_tool.tools.print import Print
from tdf_tool.tools.regular_tool import RegularTool
from tdf_tool.tools.shell_dir import ShellDir
from tdf_tool.modules.translate.flutter.text.flutter_text_translate_lint import (
    FlutterTextTranslateLint,
    TextTranslateLintResult,
)

from tdf_tool.modules.translate.flutter.text.tools.flutter_translate_integrate import (
    FlutterTranslateIntegrate,
)
import hashlib
from tdf_tool.modules.translate.tools.translate_tool import (
    MULTI_CODE_KEY,
    LanguageType,
    TranslateTool,
)
import shutil


class FlutterTextTranslateTools(FlutterTranslateToolsInterface):
    def __init__(self):
        self.__translator = TranslateTool()
        self.__i18nList = LanguageType.all()

    # 指定 模块国际化
    def translate_module(self, name, always_yes=False):
        businessModuleList = self.businessModuleList()
        self.__always_yes = always_yes
        if name in businessModuleList:
            Print.title(name + " 模块国际化脚本开始执行")
            self.__generateTranslate(name)
            Print.title(name + " 模块国际化执行完成，生成 tdf_intl 相关文件")
        else:
            Print.error(name + " 模块不在开发列表中")

    # 入口
    def __generateTranslate(self, targetModule):
        # 进入tdf_intl目录
        # tdf_intl文件夹下包含i18n文件夹，其中存放4个dart文件，分别对应四种语言
        # tdf_intl文件夹下还包含一个origin.txt文件，用于存放需要转化的文案，每个文案为一行
        ShellDir.goInModuleLibDir(targetModule)
        if not os.path.exists("tdf_intl"):
            os.mkdir("tdf_intl")
        os.chdir("tdf_intl")
        tdfIntlDir = PlatformTools.curPath()

        # 如果没有i18n文件夹则生成
        self.__generate_i18n_files(tdfIntlDir, targetModule)

        # 获取 lint 结果
        self.result: TextTranslateLintResult = (
            FlutterTextTranslateLint.get_lint_module_result(targetModule)
        )

        # 检查是否有单引号字符串
        self.__check_apostrophe_strs(targetModule)

        # 检查是否有const的中文字符串
        self.__check_const_chinese_strs(targetModule)

        # 检查是否有未使用 intl 的中文字符串
        self.__check_un_intl_strs(targetModule)

        # 检查是否有 import 错误的文件
        self.__check_err_intl_import(targetModule)

        # 是否更新 i18n.dart 文件
        self.__check_need_update_json(tdfIntlDir, targetModule)

        # 删除 json 中未用到的国际化字符串
        self.__check_delete_un_use_json(tdfIntlDir, targetModule)

        # 通过 i18n.dart 生成各个翻译后的 dart 文件
        self.__generate_translate_dart_file(tdfIntlDir, targetModule)

        # 更新 excel 文件
        self.__update_excel_file(tdfIntlDir, targetModule)

    # 如果没有i18n文件夹则生成
    def __check_delete_un_use_json(self, tdfIntlDir, targetModule):
        Print.title("开始检查 i18n.dart 中是否有多余的键值对")
        # 枚举中的中文字符串，在lint中要去掉这些
        unused_intl_json = [
            i for i in self.result.unused_json if i not in self.result.enum_chinese
        ]
        if len(unused_intl_json) <= 0:
            return

        Print.warning("i18n.dart 中有以下字符串没有使用到：")
        Print.str(unused_intl_json)

        input_str = "N"
        if self.__always_yes:
            input_str = "Y"
        else:
            input_str = input("是否删除 i18n.dart 中多余的键值对？(y/n)：")
        if input_str != "Y" and input_str != "y":
            return

        intl_dart_path = tdfIntlDir + "/i18n.dart"
        if not os.path.exists(intl_dart_path):
            return

        json_data = self.getDartFileParamsJson(intl_dart_path, MULTI_CODE_KEY)

        # 删除多余的key
        for key in unused_intl_json:
            if key in json_data:
                Print.str("删除 i18n.dart 中 " + key + " 键值对")
                del json_data[key]

        # 写入json数据
        initF = open(intl_dart_path, "w+", encoding="utf-8")
        initF.write(self.generateDartMapFile(MULTI_CODE_KEY, json_data))
        initF.close()
        os.system("dart format {0}".format(intl_dart_path))

    # 生成 i18n 相关的文件
    def __generate_i18n_files(self, tdfIntlDir, targetModule):
        # 修改map的名字
        def __changeMapName(file_path: str, old_string: str, new_string: str):
            # 读取文件内容
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            # 执行替换 - 将旧字符串替换为新字符串
            new_content = content.replace(
                f"Map<String, String> {old_string}Map =",
                f"Map<String, String> {new_string}Map =",
            )
            # 将修改后的内容写回文件
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(new_content)

        Print.title("开始生成 i18n 相关的文件")
        if not os.path.exists("i18n"):
            os.mkdir("i18n")

        if not os.path.exists("i18n.dart"):
            Print.str("生成" + "i18n.dart 文件")
            dart_file_path = tdfIntlDir + "/i18n.dart"
            json_data = {}
            if os.path.exists("i18n.json"):
                # 将之前的json文件转移到dart中
                jsonF = open("i18n.json", "r", encoding="utf-8")
                json_str = jsonF.read()
                json_data = json.loads(json_str, strict=False)
                jsonF.close()
                os.remove("i18n.json")
            initF = open(dart_file_path, "w+", encoding="utf-8")
            initF.write(self.generateDartMapFile(MULTI_CODE_KEY, json_data))
            initF.close()

        for value in self.__i18nList:
            i18nType: LanguageType = value
            os.chdir(tdfIntlDir + "/i18n")
            targetFileName = targetModule + "_" + i18nType.str() + ".dart"

            if not os.path.exists(targetFileName):
                # 兼容数据，将之前的es.dart、it.dart文件迁移到es_ES.dart、it_IT.dart
                it_lang_path = targetModule + "_it.dart"
                es_lang_path = targetModule + "_es.dart"
                if value == LanguageType.it_IT and os.path.exists(it_lang_path):
                    os.rename(it_lang_path, targetFileName)
                    __changeMapName(targetFileName, "it", i18nType.str())
                elif value == LanguageType.es_ES and os.path.exists(es_lang_path):
                    os.rename(es_lang_path, targetFileName)
                    __changeMapName(targetFileName, "es", i18nType.str())
                else:
                    Print.str("生成" + targetFileName + " 文件")
                    newI18nFile = open(targetFileName, "w+")
                    newI18nFile.write(self.generateDartMapFile(i18nType.str(), {}))
                    newI18nFile.close()

    def __check_const_chinese_strs(self, targetModule):
        Print.title("检查是否使用const修饰的中文字符串")
        if len(self.result.const_chinese) > 0:
            const_chinese_strs = []
            for i in self.result.const_chinese:
                const_chinese_strs += i.const_chinese_strs
            Print.line()
            Print.str(const_chinese_strs)
            Print.line()
            input_str = "N"
            if self.__always_yes:
                input_str = "Y"
            else:
                input_str = input(
                    "检查到有以上中文有使用到const修饰，是否删除const修饰符 ？(Y 为确认)："
                )
            if input_str == "Y" or input_str == "y":
                for i in self.result.const_chinese:
                    Print.title("开始替换的文件：" + i.file_path.split("/")[-1])
                    read_file = open(i.file_path, "r", encoding="utf-8")
                    new_file_content = read_file.read()

                    new_file_content = RegularTool.delete_const(
                        new_file_content, const_chinese_strs
                    )

                    read_file.close()
                    with open(i.file_path, "w+", encoding="utf-8") as originF:
                        originF.write(new_file_content)
                        originF.close()
                    os.system("dart format {0}".format(i.file_path))

    # 检查是否有单引号字符串
    def __check_apostrophe_strs(self, targetModule):
        Print.title("检查是否使用单引号的字符串")
        if len(self.result.apostrophes) > 0:
            apostrophe_strs = []
            for i in self.result.apostrophes:
                apostrophe_strs += i.apostrophe_strs
            Print.line()
            Print.str(apostrophe_strs)
            Print.line()
            input_str = "N"
            if self.__always_yes:
                input_str = "Y"
            else:
                input_str = input(
                    "检查到有以上有使用到单引号，是否自动替换为双引号 ？(Y 为确认)："
                )

            if input_str == "Y" or input_str == "y":
                for i in self.result.apostrophes:
                    Print.title("开始替换的文件：" + i.file_path.split("/")[-1])
                    read_file = open(i.file_path, "r", encoding="utf-8")
                    new_file_content = read_file.read()

                    new_file_content = RegularTool.replace_apostrophe_strs(
                        new_file_content, apostrophe_strs
                    )

                    read_file.close()
                    with open(i.file_path, "w+", encoding="utf-8") as originF:
                        originF.write(new_file_content)
                        originF.close()
                    os.system("dart format {0}".format(i.file_path))

    # 检查是否有错误导入的 import
    def __check_err_intl_import(self, targetModule):
        Print.title("检查是否有错误导入的 import")
        right_import = FlutterTextTranslateLint.get_module_import_str(targetModule)
        if len(self.result.imports) > 0:
            err_imports = []
            for i in self.result.imports:
                err_imports += i.import_strs
            Print.line()
            Print.str(err_imports)
            Print.line()
            input_str = "N"
            if self.__always_yes:
                input_str = "Y"
            else:
                input_str = input(
                    "检查到有以上 import 错误，是否自动替换 ？(Y 为确认)："
                )

            if input_str == "Y" or input_str == "y":
                for i in self.result.imports:
                    Print.title("开始替换 import 的文件：" + i.file_path.split("/")[-1])
                    read_file = open(i.file_path, "r", encoding="utf-8")
                    file_content = read_file.read()
                    Print.str("文件：" + i.file_path.split("/")[-1] + "开始替换 import")
                    file_content = RegularTool.replace_intl_imports(
                        file_content, right_import, targetModule
                    )
                    read_file.close()
                    with open(i.file_path, "w+", encoding="utf-8") as originF:
                        originF.write(file_content)
                        originF.close()
                    os.system("dart format {0}".format(i.file_path))

    # 检查是否有未使用 intl 的中文字符串
    def __check_un_intl_strs(self, targetModule):
        right_import = FlutterTextTranslateLint.get_module_import_str(targetModule)
        Print.title("检查是否有未使用 intl 的中文字符串")
        if len(self.result.un_intl_list) > 0:
            un_intl_list = []
            for i in self.result.un_intl_list:
                un_intl_list += i.un_intl_strs
            Print.line()
            Print.str(un_intl_list)
            Print.line()
            input_str = "N"
            if self.__always_yes:
                input_str = "Y"
            else:
                input_str = input(
                    "检查到有以上中文字符串没使用 intl，是否自动加上 .intl？(Y 为确认)："
                )
            if input_str == "Y" or input_str == "y":
                # 将中文枚举转换成map[file_path:str]，给后面使用，防止在枚举中加上.intl
                chinese_enum_map = {
                    i.file_path: i.enum_strs for i in self.result.chinese_enums
                }

                for i in self.result.un_intl_list:
                    Print.title("开始替换的文件：" + i.file_path.split("/")[-1])
                    read_file = open(i.file_path, "r", encoding="utf-8")
                    new_file_content = read_file.read()
                    lint_file_content = RegularTool.delete_remark(
                        new_file_content
                    ).lstrip()
                    # 添加 import
                    if not new_file_content.__contains__(
                        right_import
                    ) and not lint_file_content.startswith("part of"):
                        new_file_content = right_import + "\n" + new_file_content

                    # 替换 intl
                    for str in i.un_intl_strs:
                        Print.str(
                            "文件："
                            + i.file_path.split("/")[-1]
                            + " "
                            + str
                            + " 添加 intl 后缀"
                        )
                    # 先将枚举替换成md5，防止被加上.intl
                    enum_strs = chinese_enum_map.get(i.file_path, [])
                    md5_enum_strs_map: dict[str:str] = {}
                    for enum_str in enum_strs:
                        md5_str = f"【【{hashlib.md5(enum_str.encode('utf-8')).hexdigest()}】】"
                        new_file_content = new_file_content.replace(enum_str, md5_str)
                        md5_enum_strs_map[md5_str] = enum_str

                    # 替换字符，加上 .intl
                    new_file_content = RegularTool.replace_chinese_strs(
                        new_file_content, i.un_intl_strs
                    )

                    # 将md5的枚举恢复
                    for enum_str_md5 in md5_enum_strs_map.keys():
                        new_file_content = new_file_content.replace(
                            enum_str_md5, md5_enum_strs_map[enum_str_md5]
                        )

                    # 删除多个 .intl 结尾
                    new_file_content = RegularTool.replace_multi_intl(new_file_content)

                    read_file.close()
                    with open(i.file_path, "w+", encoding="utf-8") as originF:
                        originF.write(new_file_content)
                        originF.close()
                    os.system("dart format {0}".format(i.file_path))

    # 检查是否更新 i18n.dart 文件
    def __check_need_update_json(self, tdfIntlDir, targetModule):
        Print.title("检查是否更新 i18n.dart 文件")
        if (
            len(self.result.new_intl_strs) > 0
            or len(self.result.un_intl_list) > 0
            or len(self.result.enum_chinese) > 0
        ):
            un_intl_list = self.result.new_intl_strs
            un_intl_list += self.result.enum_chinese
            for i in self.result.un_intl_list:
                un_intl_list += i.un_intl_strs
            # 没有添加到json中的国际化字段
            new_un_intl_list = list(set(un_intl_list) - set(self.result.unused_json))
            add_input_str = "N"
            if len(new_un_intl_list) > 0:
                Print.warning("发现以下未添加到intl.dart中的国际化字段:")
                Print.line()
                Print.str(new_un_intl_list)
                Print.line()
                add_input_str = "N"
                if self.__always_yes:
                    add_input_str = "Y"
                else:
                    add_input_str = input(
                        "检查到有以上国际化字符串没加入到 i18n.dart，是否自动加入？(Y 为确认)："
                    )

            if add_input_str == "Y" or add_input_str == "y":
                dart_file_name = tdfIntlDir + "/i18n.dart"
                json_data = self.getDartFileParamsJson(dart_file_name, MULTI_CODE_KEY)
                with open(dart_file_name, "w+", encoding="utf-8") as originF:
                    # 添加
                    if add_input_str == "Y" or add_input_str == "y":
                        for i in new_un_intl_list:
                            # 因为正则出来的带转义符，必须去掉转义符后对比
                            i = RegularTool.decode_escapes(i)
                            if not i in json_data.keys():
                                # value后面需要改成multiCode
                                json_data[i] = i
                    originF.write(self.generateDartMapFile(MULTI_CODE_KEY, json_data))
                    originF.close()
                    os.system("dart format {0}".format(dart_file_name))
                Print.title("i18n.dart 更新成功")

    # 通过 i18n.dart 生成各个翻译后的 dart 文件
    def __generate_translate_dart_file(self, tdfIntlDir: str, targetModule: str):
        Print.title("开始通过 i18n.dart 生成各个翻译后的 dart 文件")
        dart_file_name = tdfIntlDir + "/i18n.dart"
        json_data = self.getDartFileParamsJson(dart_file_name, MULTI_CODE_KEY)

        # 遍历i18n目录下的四个存放语言的dart文件
        for value in self.__i18nList:
            i18nType: LanguageType = value
            os.chdir(tdfIntlDir + "/i18n")
            Print.line()
            targetFileName = targetModule + "_" + i18nType.str() + ".dart"

            paramsJson = self.getDartFileParamsJson(
                targetFileName,
                i18nType.str(),
            )

            os.chdir(tdfIntlDir + "/i18n")

            # 多线程翻译
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # 准备翻译任务
                futures = {}
                for key in json_data.keys():
                    if len(paramsJson) > 0 and key in paramsJson:
                        continue

                    if i18nType.name == LanguageType.zh_CN.name:
                        paramsJson[r"{0}".format(key)] = r"{0}".format(key)
                    else:
                        # 提交翻译任务到线程池
                        future = executor.submit(self.__tdf_translate, key, i18nType)
                        futures[future] = key

                # 处理完成的任务
                for future in concurrent.futures.as_completed(futures):
                    key = futures[future]
                    translatedStr = future.result()
                    paramsJson[r"{0}".format(key)] = r"{0}".format(translatedStr)

            # 去除所有翻译失败，value为空的key
            if isinstance(paramsJson, dict):
                keyList = list(paramsJson.keys())
                for k in keyList:
                    if not paramsJson[k]:
                        del paramsJson[k]

            with open(targetFileName, "a", encoding="utf-8") as targetFile:
                targetFile.seek(0)  # 定位
                targetFile.truncate()  # 清空文件
                targetFile.write(self.generateDartMapFile(i18nType.str(), paramsJson))
            os.system("dart format {0}".format(targetFileName))

            self.__generateManagerClass(targetModule)

    def __generateManagerClass(self, moduleName):
        Print.str("生成" + moduleName + "_i18n.dart" + " 文件")
        # 生成manager类
        ShellDir.goInModuleIntlDir(moduleName)

        with open(moduleName + "_i18n.dart", "w+", encoding="utf-8") as managerF:
            managerF.truncate()
            managerF.write(
                LanguageType.text_dart_file(
                    moduleName,
                    self.getManagerClassName(moduleName),
                )
            )

    def __tdf_translate(self, content: str, dest_lan: LanguageType):
        try:
            text = self.__translator.translate(
                content, src=LanguageType.zh_CN, dest=dest_lan
            )
            return text
        except Exception as e:
            Print.str("{0} 翻译失败：{1}".format(content, e))
            return ""

    # 更新excel文件
    def __update_excel_file(self, tdfIntlDir, targetModule):
        Print.title(targetModule + " 模块整合开始执行")
        # 生成excel文件
        excel_dict = self.generateI18nExcelDict(f"{tdfIntlDir}/i18n/{targetModule}")
        # 将excel_dict写入excel文件
        GitlabServeFileTool.write_text_excel(excel_dict, targetModule)

    # 整合各个模块翻译文件到一起
    def integrate(self):
        self.integrate: FlutterTranslateIntegrate = FlutterTranslateIntegrate()
        ShellDir.goInShellDir()
        businessModuleList = self.businessModuleList()

        Print.str("检测到以下模块可整合翻译文件：")
        Print.str(businessModuleList)

        while True:
            targetModule = input(
                "请输入需要执行整合的模块名(input ! 退出，all 所有模块执行)："
            )
            all_dict = self.integrate.integrate_json_root()
            if targetModule == "!" or targetModule == "！":
                exit(0)
            elif targetModule == "all":
                all_dict = self.integrate.integrate_json_root()
                for module in businessModuleList:
                    module_dict = self.__integrate_module(module)
                    ####
                    all_dict = self.integrate.merge_dict(module_dict, all_dict)
            else:
                module_dict = self.__integrate_module(targetModule)
                all_dict = self.integrate.merge_dict(module_dict, all_dict)
            self.integrate.write_dict_to_json(all_dict)
            self.integrate.upload_json()
            exit(0)

    # 指定 模块国际化
    def __integrate_module(self, name: str) -> dict[str, dict[str, str]]:
        ShellDir.goInShellDir()
        businessModuleList = self.businessModuleList()
        if name in businessModuleList:
            Print.title(name + " 模块整合开始执行")
            # pod = list(filter(lambda x: x.name == name, batchPodList))[0]
            Print.title(name + " 模块整合完成")
            return self.integrate.integrate_module(name)
        else:
            Print.error(name + " 模块不在开发列表中")

    def clear_i18n_files(self):
        ShellDir.goInShellDir()
        businessModuleList = self.businessModuleList()

        Print.str("检测到以下模块可清除翻译文件夹：")
        Print.str(businessModuleList)

        while True:
            targetModule = input(
                "请输入需要执行整合的模块名(input ! 退出，all 所有模块执行)："
            )
            if targetModule == "!" or targetModule == "！":
                exit(0)
            elif targetModule == "all":
                for module in businessModuleList:
                    self.__clear_i18n_module(module)
            else:
                self.__clear_i18n_module(targetModule)
            exit(0)

    def __clear_i18n_module(self, targetModule):
        ShellDir.goInModuleLibDir(targetModule)
        Print.title("开始删除 i18n 相关的文件")
        if os.path.exists("tdf_intl"):
            shutil.rmtree("tdf_intl")
            Print.str("删除 tdf_intl 文件夹完成")
