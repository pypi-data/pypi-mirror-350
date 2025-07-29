from tdf_tool.modules.translate.flutter.flutter_translate_lint import (
    FlutterTranslateLintFactory,
)
from tdf_tool.tools.shell_dir import ProjectType, ShellDir
from tdf_tool.modules.translate.ios.ios_translate_lint import iOSTranslateLint


class TranslateLint:
    """
    国际化相关：检测源码中是否还有没国际化的文案
    """

    def start(self, all_module=False):
        """
        以交互的方式选择需要 lint 的模块
        """
        ShellDir.dirInvalidate()
        project_type = ShellDir.getProjectType()
        if project_type == ProjectType.FLUTTER:
            FlutterTranslateLintFactory().start(all_module)
        elif project_type == ProjectType.IOS:
            iOSTranslateLint.start()

    def module(self, name: str):
        """
        指定模块 lint
        """
        ShellDir.dirInvalidate()
        project_type = ShellDir.getProjectType()
        if project_type == ProjectType.FLUTTER:
            FlutterTranslateLintFactory().lint_module(name)
        elif project_type == ProjectType.IOS:
            iOSTranslateLint.module(name)

    def path(self, path: str):
        """
        指定模块路径 lint，路径为 lib 路径
        """
        project_type: ProjectType
        if path == "lib":
            project_type = ProjectType.FLUTTER
        else:
            project_type = ShellDir.getProjectType()

        if project_type == ProjectType.FLUTTER:
            FlutterTranslateLintFactory().lint_path(path)
        elif project_type == ProjectType.IOS:
            iOSTranslateLint.path(path)
