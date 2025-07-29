from tdf_tool.tools.shell_dir import ProjectType, ShellDir
from tdf_tool.modules.multi_code.ios.ios_i18n_lint import iOSI18nLint
from tdf_tool.modules.multi_code.flutter.flutter_multi_code_lint import (
    FlutterMultiCodeLint,
)


class i18nLint:
    """iOS国际化lint，检查出来是否有没有进行服务端国际化的key"""

    def start(self):
        """交互式lint国际化文件"""
        ShellDir.dirInvalidate()
        projectType = ShellDir.getProjectType()
        if projectType == ProjectType.FLUTTER:
            FlutterMultiCodeLint().start()
        elif projectType == ProjectType.IOS:
            iOSI18nLint().start()

    def module(self, name: str):
        """指定 模块国际化lint

        Args:
            name (str): 开发中的模块名
        """
        ShellDir.dirInvalidate()
        projectType = ShellDir.getProjectType()
        if projectType == ProjectType.FLUTTER:
            FlutterMultiCodeLint().module(name)
        elif projectType == ProjectType.IOS:
            iOSI18nLint().module(name)

    def path(self, path: str):
        """指定 路径国际化lint

        Args:
            path (str): 指定路径
        """
        ShellDir.dirInvalidate()
        projectType = ShellDir.getProjectType()
        if projectType == ProjectType.FLUTTER:
            FlutterMultiCodeLint().path(path)
        elif projectType == ProjectType.IOS:
            iOSI18nLint().path(path)
