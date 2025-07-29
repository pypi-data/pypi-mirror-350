from tdf_tool.modules.multi_code.flutter.flutter_multi_code_tools import (
    FlutterMultiCodeTools,
)
from tdf_tool.modules.multi_code.tools.serve_file import GitlabServeFileTool
from tdf_tool.modules.translate.flutter.flutter_tranalate_interface import (
    FlutterTranslateToolsInterface,
)
from tdf_tool.modules.translate.flutter.text.flutter_text_translate_tools import (
    FlutterTextTranslateTools,
)
from tdf_tool.modules.translate.flutter.resource.flutter_res_translate_tools import (
    FlutterResTranslateTools,
)

from tdf_tool.tools.print import Print


class FlutterTranslateToolsFactory(FlutterTranslateToolsInterface):

    def __init__(self):
        # 文本翻译工具
        self._text_translate_tools = FlutterTextTranslateTools()
        # 资源翻译工具
        self._res_translate_tools = FlutterResTranslateTools()
        #  multiCode 工具
        self._multi_code_tools = FlutterMultiCodeTools()

    def translate(self, targetModule, all_module=False, always_yes=False):
        businessModuleList = self.businessModuleList()

        Print.str("检测到以下模块可执行国际化脚本：")
        Print.str(businessModuleList)
        while True:
            targetModule = "!"
            if all_module:
                targetModule = "all"
            else:
                targetModule = input(
                    "请输入需要执行国际化脚本的模块名(input ! 退出，all 所有模块执行)："
                )

            if targetModule == "!" or targetModule == "！":
                exit(0)
            elif targetModule == "all":
                for module in businessModuleList:
                    self.translate_module(module, always_yes)
                exit(0)
            else:
                self.translate_module(targetModule, always_yes)
                exit(0)

    def translate_module(self, name, always_yes=False):
        # 拉取远程国际化code映射文件
        GitlabServeFileTool.pull_form_server()
        # 如果其他开发者正在进行code生成，防止code重复
        if GitlabServeFileTool.is_in_operation():
            Print.error("其他开发者正在进行code生成，防止code重复，请稍后再试")
        GitlabServeFileTool.update_in_operation(True)
        GitlabServeFileTool.upload_to_server()
        try:
            # 翻译资源文件
            self._res_translate_tools.translate_module(name, always_yes)
            # 翻译文本文件
            self._text_translate_tools.translate_module(name, always_yes)
            # 生成MultiCode
            self._multi_code_tools.translate_module(name, always_yes)
            GitlabServeFileTool.update_in_operation(False)
        except SystemExit:
            Print.str("\n正在优雅地退出...")
            GitlabServeFileTool.update_in_operation(False)
        except KeyboardInterrupt:
            Print.str("\n检测到 Ctrl+C，正在优雅地退出...")
            GitlabServeFileTool.update_in_operation(False)
        finally:
            # 上传MultiCode到服务端
            GitlabServeFileTool.upload_to_server()

    def integrate(self):
        self._res_translate_tools.integrate()
        self._text_translate_tools.integrate()

    def clear_i18n_files(self):
        self._res_translate_tools.clear_i18n_files()
        self._text_translate_tools.clear_i18n_files()
