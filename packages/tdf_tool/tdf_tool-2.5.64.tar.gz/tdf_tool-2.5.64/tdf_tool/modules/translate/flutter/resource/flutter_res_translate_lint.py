import os
from tdf_tool.modules.translate.flutter.flutter_tranalate_interface import (
    FlutterTranslateDartFileTool,
    FlutterTranslateModuleTool,
)
from tdf_tool.modules.translate.flutter.flutter_translate_lint_interface import (
    FlutterTranslateLintInterface,
    TranslateLintApostrophe,
)
from tdf_tool.modules.translate.tools.translate_tool import MULTI_CODE_KEY
from tdf_tool.tools.print import Print
from tdf_tool.tools.regular_tool import RegularTool
from tdf_tool.tools.shell_dir import ShellDir


class ResTranslateLintIntl:
    def __init__(self, file_path: str, un_intl_strs: list[str]):
        # 未国际化文件路径
        self.file_path = file_path
        # 文件中没有国际化的图片url
        self.un_intl_strs = un_intl_strs


class ResTranslateLintImport:
    def __init__(self, file_path: str, import_strs: list[str]):
        # import 错误的文件路径
        self.file_path = file_path
        # import 错误的字符串
        self.import_strs = import_strs


class ResTranslateLintConst:
    def __init__(self, file_path: str, const_strs: list[str]):
        # 常量中有图片url的文件路径
        self.file_path = file_path
        # 常量中有图片url的字符串
        self.const_strs = const_strs


class ResTranslateLintResult:
    def __init__(
        self,
        un_intl_list: list[ResTranslateLintIntl],
        new_intl_strs: list[str],
        unused_json: list[str],
        imports: list[ResTranslateLintImport],
        const_list: list[ResTranslateLintConst],
        apostrophes: list[TranslateLintApostrophe],
    ):
        # 没有使用 .resIntl 修饰的中文字符串，不包含枚举中的中文
        self.un_intl_list = un_intl_list
        # 与json文件对比后，新的使用 .resIntl 修饰的中文字符串
        self.new_intl_strs = list(set(new_intl_strs))
        # 不符合规范的 import
        self.imports = imports
        # 使用const声明的图片url
        self.const_list = const_list
        # i18n.dart 中没用到的图片资源url
        self.unused_json = list(set(unused_json))
        # 单引号
        self.apostrophes = list(set(apostrophes))


class FlutterResTranslateLint(FlutterTranslateLintInterface):
    def lint_all(self):
        """
        全部模块 lint
        """
        results = []
        pass_result = True
        for module in self.businessModuleList():
            result = FlutterResTranslateLint.get_lint_module_result(module)
            results.append(result)
            if not FlutterResTranslateLint.__lint_result(result):
                pass_result = False
                Print.error(module + " 模块国际化 lint 失败", shouldExit=False)
            else:
                Print.title(module + " 模块国际化 lint 成功")
        if pass_result:
            print("\n")
            Print.title("国际化 lint 通过")
        else:
            Print.error("国际化 lint 失败")

    def lint_module(self, name: str):
        """
        指定模块 lint
        """
        if not self.can_translate(name):
            Print.warning(name + " 模块不需要国际化")
            return
        result = FlutterResTranslateLint.get_lint_module_result(name)
        if FlutterResTranslateLint.__lint_result(result):
            Print.stage(name + " 模块国际化 lint 通过")
        else:
            Print.error(name + " 模块国际化 lint 失败")

    def lint_path(self, path: str):
        """
        指定模块路径 lint，路径为 lib 路径
        """
        if not self.can_translate_lib_path(path):
            Print.warning(path + " 不需要国际化")
            return
        result = FlutterResTranslateLint.__lint_intl_path(path)
        if FlutterResTranslateLint.__lint_result(result):
            Print.title(path + " 路径国际化 lint 通过")
        else:
            Print.error(path + " 路径国际化lint 失败")

    @staticmethod
    def get_lint_module_result(module_name: str) -> ResTranslateLintResult:
        Print.title(module_name + " 模块国际化 lint 开始执行")
        target_path = ShellDir.getModuleLibDir(module_name)
        if os.path.exists(target_path):
            return FlutterResTranslateLint.__lint_intl_path(target_path)
        else:
            Print.error(target_path + "路径不存在")

    # 指定路径 lint，path 的必须是 lib 文件
    @staticmethod
    def __lint_intl_path(path: str) -> ResTranslateLintResult:
        # 没有使用 .resIntl 修饰的图片url
        un_intl_list: list[ResTranslateLintIntl] = []
        # 使用 .resIntl 修饰的图片url
        intl_strs: list[str] = []  # type: ignore
        # 所有的 dart 文件路径
        dart_files: list[str] = []  # type: ignore
        # 使用const声明的图片url
        const_urls: list[ResTranslateLintConst] = []
        # 不符合的 imports
        imports: list[ResTranslateLintImport] = []
        # 单引号
        apostrophes: list[TranslateLintApostrophe] = []

        module_name = ShellDir.getModuleNameFromYaml(path + "/../pubspec.yaml")
        right_import = FlutterResTranslateLint.get_module_import_str(module_name)

        i18n_json: dict = FlutterResTranslateLint.__get_i18n_json(path)
        Print.stage("lint 路径：" + path)
        for root, __, files in os.walk(path):
            for file in files:
                # 过滤掉 tdf_res_intl 目录下的 dart 文件
                if FlutterTranslateModuleTool.filter_file(file, root):
                    dart_files.append(root + "/" + file)
        for file in dart_files:
            f = open(file)
            file_content = f.read()

            file_content = RegularTool.delete_remark(file_content)
            # 所有的 intl import
            all_imports = RegularTool.find_res_intl_imports(file_content)
            # 错误的 res_intl import
            err_imports = list(filter(lambda x: x != right_import, all_imports))
            if len(err_imports) > 0:
                un_import = ResTranslateLintImport(file, err_imports)
                imports.append(un_import)

            # lines = file_content.splitlines()
            # file_content = "".join(lines)
            file_content = RegularTool.delete_track(file_content)
            file_content = RegularTool.delete_router(file_content)
            file_content = RegularTool.delete_widgetsDoc(file_content)
            file_content = RegularTool.delete_noTranslDoc(file_content)
            file_content = RegularTool.delete_deprecated(file_content)

            # 寻找使用 const 声明的中文字符串
            const_strs = RegularTool.find_const_image_url(file_content)
            if len(const_strs) > 0:
                const_urls.append(ResTranslateLintConst(file, const_strs))

            # 寻找单引号字符串
            apostrophe_strs = RegularTool.find_res_apostrophe_strs(file_content)
            if len(apostrophe_strs) > 0:
                apostrophe = TranslateLintApostrophe(file, apostrophe_strs)
                apostrophes.append(apostrophe)

            # 寻找加上 .resIntl 的文案，并删除掉，以免影响 下面的操作
            _intl_strs = RegularTool.find_res_intl_str(file_content)
            intl_strs += _intl_strs
            file_content = RegularTool.delete_res_intl_str(file_content)

            # 寻找没有国际化的 文案
            _un_intl_strs = RegularTool.find_image_url_str(file_content)

            if len(_un_intl_strs) > 0:
                _un_intl_list = ResTranslateLintIntl(file, _un_intl_strs)
                un_intl_list.append(_un_intl_list)
            f.close()

        # intl_strs 去重
        intl_strs = list(set(intl_strs))
        new_intl_strs = []
        # 对比加上 .resIntl 的文案 和 res_i18n.dart 里面的差异
        unused_json = list(i18n_json.keys())
        for key in intl_strs:
            # 因为正则出来的带转义符，必须去掉转义符后对比
            key = RegularTool.decode_escapes(key)
            if key in unused_json:
                unused_json.remove(key)
            else:
                new_intl_strs.append(key)

        return ResTranslateLintResult(
            un_intl_list,
            new_intl_strs,
            unused_json,
            imports,
            const_urls,
            apostrophes,
        )

    # 获取模块正确的 import 语句
    def get_module_import_str(module_name: str) -> str:
        return "import 'package:{name}/tdf_res_intl/{name}_res_i18n.dart';".format(
            name=module_name
        )

    # 获取 res_i18n.dart中的数据
    def __get_i18n_json(path: str) -> dict[str:str]:
        target_path = path + "/tdf_res_intl/res_i18n.dart"
        if os.path.exists(target_path):
            return FlutterTranslateDartFileTool.getDartFileParamsJson(
                target_path, MULTI_CODE_KEY
            )
        else:
            return {}

    # 校验 lint 的结果
    def __lint_result(result: ResTranslateLintResult) -> bool:
        if len(result.apostrophes) > 0:
            Print.warning("使用到了单引号字符串，请统一修改为双引号")
            for i in result.apostrophes:
                file_name = i.file_path.split(r"/")[-1]
                Print.title(file_name + " 文件中有以下未国际化的字符串：")
                Print.str(i.apostrophe_strs)

        if len(result.unused_json) > 0:
            Print.warning("图片资源的i18n.dart 中有以下字符串没有使用到：")
            Print.str(result.unused_json)

        if len(result.un_intl_list) > 0:
            Print.warning("以下文件中有没国际化的图片资源：")
            for i in result.un_intl_list:
                file_name = i.file_path.split(r"/")[-1]
                Print.warning(file_name + " 文件中有以下未国际化的图片资源：")
                Print.str(i.un_intl_strs)

        if len(result.new_intl_strs) > 0:
            Print.warning("以下 .resIntl 修饰的图片url没有添加到 i18n.dart 中：")
            Print.str(result.new_intl_strs)

        if len(result.imports) > 0:
            Print.warning("以下文件中有没不符合规范的 import ：")
            for i in result.imports:
                file_name = i.file_path.split(r"/")[-1]
                Print.title(file_name + " 文件中有以下不符合规范的 import ：")
                Print.str(i.import_strs)

        if len(result.const_list):
            Print.warning("以下文件中有使用 const 声明图片资源：")
            for i in result.const_list:
                file_name = i.file_path.split(r"/")[-1]
                Print.title(file_name + " 文件中有使用const修饰的图片资源：")
                Print.str(i.const_strs)

        return (
            len(result.un_intl_list) == 0
            and len(result.unused_json) == 0
            and len(result.new_intl_strs) == 0
            and len(result.imports) == 0
            and len(result.const_list) == 0
            and len(result.apostrophes) == 0
        )
