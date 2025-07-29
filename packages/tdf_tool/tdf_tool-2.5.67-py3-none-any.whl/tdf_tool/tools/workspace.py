from enum import Enum
from tdf_tool.tools.print import Print
import os

from tdf_tool.tools.shell_dir import ShellDir


class ProjectType(Enum):
    FLUTTER = 1
    IOS = 2


class ProjectApp(Enum):
    REST = 1
    YUNCRSH = 2
    SUPPLYCHAIN = 3

    def decs(self) -> str:
        if self.value == 2:
            return "yun"
        elif self.value == 3:
            return "chain"
        else:
            return "rest"


class WorkSpaceTool:
    def podfile_path() -> str:
        return ShellDir.workspace() + "/Podfile"

    def get_project_app(workspace: str = None) -> ProjectApp:
        """当前项目app归属

        Returns:
            ProjectApp: 项目app归属
        """
        if workspace is None:
            workspace = ShellDir.workspace()
        app_name = workspace.split("/")[-1]
        if (
            app_name == "YunCash"
            or app_name == "flutter_yuncash_app"
            or app_name == "flutter_yuncash_module"
        ):
            return ProjectApp.YUNCRSH
        elif app_name == "TDFSupplyChainApp":
            return ProjectApp.SUPPLYCHAIN
        else:
            return ProjectApp.REST

    def get_project_type(workspace: str = None) -> ProjectType:
        """返回当前项目类型

        Returns:
            ProjectType: 项目类型
        """
        if workspace is None:
            workspace = ShellDir.workspace()
        if os.path.exists(workspace + "/Podfile"):
            return ProjectType.IOS
        elif os.path.exists(workspace + "/pubspec.yaml"):
            return ProjectType.FLUTTER
        else:
            for name in os.listdir(workspace):
                if name.endswith(".podspec"):
                    return ProjectType.IOS
            return Print.error(workspace + "路径不是iOS、flutter工程路径")
