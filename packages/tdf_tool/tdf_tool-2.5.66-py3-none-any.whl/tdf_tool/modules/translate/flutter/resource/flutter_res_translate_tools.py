import json
import os
import shutil
from tdf_tool.modules.multi_code.tools.serve_file import GitlabServeFileTool
from tdf_tool.modules.translate.flutter.flutter_translate_tools import (
    FlutterTranslateToolsInterface,
)
from tdf_tool.modules.translate.flutter.resource.flutter_res_translate_lint import (
    FlutterResTranslateLint,
    ResTranslateLintResult,
)
from tdf_tool.modules.translate.tools.translate_tool import MULTI_CODE_KEY, LanguageType
from tdf_tool.tools.platform_tools import PlatformTools
from tdf_tool.tools.print import Print
from tdf_tool.tools.regular_tool import RegularTool
from tdf_tool.tools.shell_dir import ShellDir


class FlutterResTranslateTools(FlutterTranslateToolsInterface):
    def __init__(self):
        self.__i18nList = LanguageType.all()

    def translate_module(self, name, always_yes=False):
        businessModuleList = self.businessModuleList()
        self.__always_yes = always_yes
        if name in businessModuleList:
            Print.title(name + " 模块国际化脚本开始执行")
            self.__generateTranslate(name)
            Print.title(name + " 模块国际化执行完成，生成 tdf_intl 相关文件")
        else:
            Print.error(name + " 模块不在开发列表中")

    def integrate(self):
        pass

    def __generateTranslate(self, targetModule):
        # 进入tdf_res_intl目录
        # tdf_res_intl文件夹下包含i18n文件夹，其中存放4个dart文件，分别对应四种语言
        # tdf_res_intl文件夹下还包含一个origin.txt文件，用于存放需要转化的文案，每个文案为一行
        ShellDir.goInModuleLibDir(targetModule)
        if not os.path.exists("tdf_res_intl"):
            os.mkdir("tdf_res_intl")
        os.chdir("tdf_res_intl")
        tdfIntlDir = PlatformTools.curPath()

        # 如果没有i18n文件夹则生成
        self.__generate_i18n_files(tdfIntlDir, targetModule)

        # 获取 lint 结果
        self.result: ResTranslateLintResult = (
            FlutterResTranslateLint.get_lint_module_result(targetModule)
        )

        # 检查是否有单引号字符串
        self.__check_apostrophe_strs(targetModule)

        # 检查是否有const的图片url
        self.__check_const_image_url(targetModule)

        # 检查是否有未使用 resIntl 的图片url
        self.__check_un_intl_urls(targetModule)

        # 检查是否有 import 错误的文件
        self.__check_err_intl_import(targetModule)

        # 是否更新 res_i18n.dart 文件
        self.__check_need_update_json(tdfIntlDir, targetModule)

        # 删除 res_i18n.dart 中未用到的国际化图片url
        self.__check_delete_un_use_json(tdfIntlDir, targetModule)

        # 通过 res_i18n.dart 生成各个 dart 文件
        self.__generate_dart_file(tdfIntlDir, targetModule)

        # 更新excel文件
        self.__update_excel_file(tdfIntlDir, targetModule)

    # 生成 i18n 相关的文件
    def __generate_i18n_files(self, tdfIntlDir, targetModule):
        Print.title("开始生成 i18n 相关的文件")
        if not os.path.exists("res_i18n"):
            os.mkdir("res_i18n")

        if not os.path.exists("res_i18n.dart"):
            Print.str("生成" + "res_i18n.dart 文件")
            intl_dart_path = tdfIntlDir + "/res_i18n.dart"
            initF = open(intl_dart_path, "w+", encoding="utf-8")
            initF.write(self.generateDartMapFile(MULTI_CODE_KEY, {}))
            initF.close()
            os.system("dart format {0}".format(intl_dart_path))

        for value in self.__i18nList:
            i18nType: LanguageType = value
            os.chdir(tdfIntlDir + "/res_i18n")
            targetFileName = targetModule + "_" + i18nType.str() + ".dart"

            if not os.path.exists(targetFileName):
                Print.str("生成" + targetFileName + " 文件")
                newI18nFile = open(targetFileName, "w+")
                self.generateDartMapFile(i18nType.str(), {})
                newI18nFile.close()
                os.system("dart format {0}".format(targetFileName))

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

    # 检查是否有const的图片url
    def __check_const_image_url(self, targetModule):
        Print.title("检查是否使用const修饰的图片url")
        if len(self.result.const_list) > 0:
            const_image_url_strs = []
            for i in self.result.const_list:
                const_image_url_strs += i.const_strs
            Print.line()
            Print.str(const_image_url_strs)
            Print.line()
            input_str = "N"
            if self.__always_yes:
                input_str = "Y"
            else:
                input_str = input(
                    "检查到有以上图片url有使用到const修饰，是否删除const修饰符 ？(Y 为确认)："
                )
            if input_str == "Y" or input_str == "y":
                for i in self.result.const_list:
                    Print.title("开始替换的文件：" + i.file_path.split("/")[-1])
                    read_file = open(i.file_path, "r", encoding="utf-8")
                    new_file_content = read_file.read()

                    new_file_content = RegularTool.delete_const(
                        new_file_content, const_image_url_strs
                    )

                    read_file.close()
                    with open(i.file_path, "w+", encoding="utf-8") as originF:
                        originF.write(new_file_content)
                        originF.close()
                    os.system("dart format {0}".format(i.file_path))

    # 检查是否有未使用 intl 的中文字符串
    def __check_un_intl_urls(self, targetModule):
        right_import = FlutterResTranslateLint.get_module_import_str(targetModule)
        Print.title("检查是否有未使用 resIntl 的图片url")
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
                    "检查到有以上图片url没使用 resIntl，是否自动加上 .resIntl？(Y 为确认)："
                )
            if input_str == "Y" or input_str == "y":
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
                            + " 添加 resIntl 后缀"
                        )
                    # 替换字符，加上 .resIntl
                    new_file_content = RegularTool.replace_res_intl_strs(
                        new_file_content, i.un_intl_strs
                    )

                    # 删除多个 .resIntl 结尾
                    new_file_content = RegularTool.replace_multi_res_intl(
                        new_file_content
                    )

                    read_file.close()
                    with open(i.file_path, "w+", encoding="utf-8") as originF:
                        originF.write(new_file_content)
                        originF.close()
                    os.system("dart format {0}".format(i.file_path))

    # 检查是否有错误导入的 import
    def __check_err_intl_import(self, targetModule):
        Print.title("检查是否有错误导入的 import")
        right_import = FlutterResTranslateLint.get_module_import_str(targetModule)
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
                    file_content = RegularTool.replace_res_intl_imports(
                        file_content, right_import, targetModule
                    )

                    read_file.close()
                    with open(i.file_path, "w+", encoding="utf-8") as originF:
                        originF.write(file_content)
                        originF.close()
                    os.system("dart format {0}".format(i.file_path))

    # 检查是否更新 res_i18n.dart 文件
    def __check_need_update_json(self, tdfIntlDir, targetModule):
        Print.title("检查是否更新 res_i18n.dart 文件")
        if len(self.result.new_intl_strs) > 0 or len(self.result.un_intl_list) > 0:
            un_intl_list = self.result.new_intl_strs
            for i in self.result.un_intl_list:
                un_intl_list += i.un_intl_strs
            # 没有添加到json中的国际化字段
            new_un_intl_list = list(set(un_intl_list) - set(self.result.unused_json))
            add_input_str = "N"
            if len(new_un_intl_list) > 0:
                Print.warning("发现以下未添加到res_i18n.dart中的国际化字段:")
                Print.line()
                Print.str(new_un_intl_list)
                Print.line()
                add_input_str = "N"
                if self.__always_yes:
                    add_input_str = "Y"
                else:
                    add_input_str = input(
                        "检查到有以上国际化url没加入到 res_i18n.dart，是否自动加入？(Y 为确认)："
                    )

            if add_input_str == "Y" or add_input_str == "y":
                dart_file_name = tdfIntlDir + "/res_i18n.dart"
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
                Print.title("res_i18n.dart 更新成功")

    # 如果没有i18n文件夹则生成
    def __check_delete_un_use_json(self, tdfIntlDir, targetModule):
        Print.title("开始检查 res_i18n.dart 中是否有多余的键值对")
        unused_intl_json = self.result.unused_json
        if len(unused_intl_json) <= 0:
            return

        Print.warning("res_i18n.dart 中有以下字符串没有使用到：")
        Print.str(unused_intl_json)

        input_str = "N"
        if self.__always_yes:
            input_str = "Y"
        else:
            input_str = input("是否删除 res_i18n.dart 中多余的键值对？(y/n)：")
        if input_str != "Y" and input_str != "y":
            return

        intl_dart_path = tdfIntlDir + "/res_i18n.dart"
        if not os.path.exists(intl_dart_path):
            return

        json_data = self.getDartFileParamsJson(intl_dart_path, MULTI_CODE_KEY)

        # 删除多余的key
        for key in unused_intl_json:
            if key in json_data:
                Print.str("删除 res_i18n.dart 中 " + key + " 键值对")
                del json_data[key]

        # 写入json数据
        initF = open(intl_dart_path, "w+", encoding="utf-8")
        initF.write(self.generateDartMapFile(MULTI_CODE_KEY, json_data))
        initF.close()
        os.system("dart format {0}".format(intl_dart_path))

    # 通过 res_i18n.dart 生成各个 dart 文件
    def __generate_dart_file(self, tdfIntlDir: str, targetModule: str):
        Print.title("开始通过 res_i18n.dart 生成各个翻译后的 dart 文件")
        # 遍历i18n目录下存放语言的dart文件，并生成
        for value in self.__i18nList:
            i18nType: LanguageType = value
            os.chdir(tdfIntlDir + "/res_i18n")
            Print.line()
            targetFileName = targetModule + "_" + i18nType.str() + ".dart"
            # 获取dart文件内的数据
            paramsJson = self.getDartFileParamsJson(
                targetFileName,
                i18nType.str(),
            )

            os.chdir(tdfIntlDir + "/res_i18n")

            with open(targetFileName, "a", encoding="utf-8") as targetFile:
                targetFile.seek(0)  # 定位
                targetFile.truncate()  # 清空文件
                targetFile.write(self.generateDartMapFile(i18nType.str(), paramsJson))
            os.system("dart format {0}".format(targetFileName))

        self.__generateManagerClass(targetModule)

    def __generateManagerClass(self, moduleName):
        Print.str("生成" + moduleName + "_res_i18n.dart" + " 文件")
        # 生成manager类
        ShellDir.goInModuleResIntlDir(moduleName)

        with open(moduleName + "_res_i18n.dart", "w+", encoding="utf-8") as managerF:
            managerF.truncate()
            managerF.write(
                LanguageType.res_dart_file(
                    moduleName,
                    self.getManagerClassName(moduleName),
                )
            )

    def clear_i18n_files(self):
        ShellDir.goInShellDir()
        businessModuleList = self.__businessModuleList()

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
        if os.path.exists("tdf_res_intl"):
            shutil.rmtree("tdf_res_intl")
            Print.str("删除 tdf_res_intl 文件夹完成")

    # 更新excel文件
    def __update_excel_file(self, tdfIntlDir, targetModule):
        Print.title(targetModule + " 模块整合开始执行")
        # 生成excel文件
        excel_dict = self.generateI18nExcelDict(f"{tdfIntlDir}/res_i18n/{targetModule}")
        # 将excel_dict写入excel文件
        GitlabServeFileTool.write_res_excel(excel_dict, targetModule)
