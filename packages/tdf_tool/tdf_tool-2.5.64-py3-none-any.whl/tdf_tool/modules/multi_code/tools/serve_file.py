import json
import os
import pandas as pd
from tdf_tool.tools.cmd import Cmd
from tdf_tool.modules.multi_code.tools.file_util import FileUtil
from tdf_tool.tools.print import Print
from tdf_tool.tools.workspace import ProjectApp, ProjectType, WorkSpaceTool


class MultiCodeServerKeyDecs:
    def __init__(self, key, module_name, origin_key):
        self.key = key
        self.module_name = module_name
        self.origin_key = origin_key


class GitlabServeFileTool:

    # code是否正在生成中
    def is_in_operation() -> bool:
        path = GitlabServeFileTool.server_in_operation_path()
        if not os.path.exists(path):
            return False
        with open(path, encoding="utf8") as f:
            content = f.read()
            f.close()
            return content.lower() == "true"

    # 修改是否生成code的文件
    def update_in_operation(value: bool):
        path = GitlabServeFileTool.server_in_operation_path()
        with open(path, mode="w", encoding="utf8") as f:
            f.write(f"{value}")
            f.close()

    # 读取last_server_key的值
    def read_text_last_key() -> int:
        path = GitlabServeFileTool.server_text_last_key_path()
        if not os.path.exists(path):
            return 0
        else:
            with open(path, encoding="utf8") as f:
                content = f.read()
                f.close()
                return int(content)

    # 更新last_server_key的值
    def update_text_last_key(value: int):
        path = GitlabServeFileTool.server_text_last_key_path()
        with open(path, mode="w", encoding="utf8") as f:
            f.write("{}".format(value))
            f.close()

    # 读取res_last_server_key的值
    def read_res_last_key() -> int:
        path = GitlabServeFileTool.server_res_last_key_path()
        if not os.path.exists(path):
            return 0
        else:
            with open(path, encoding="utf8") as f:
                content = f.read()
                f.close()
                return int(content)

    # 更新res_last_server_key的值
    def update_res_last_key(value: int):
        path = GitlabServeFileTool.server_res_last_key_path()
        with open(path, mode="w", encoding="utf8") as f:
            f.write(f"{value}")
            f.close()

    # 将10进制的树转换成36进制的字符串
    def convert(value: int) -> str:
        """将10进制的树转换成36进制的字符串

        Args:
            value (int): 输入的十进制

        Returns:
            str: 返回的36进制字符串
        """
        if value > 46656:
            Print.error("数值不能大于 46656")
        asc_list: list[int] = []
        for i in range(3):
            if value == 0:
                # ASCII值 0-9 是 48~57
                asc_list.insert(0, 48)
                continue
            mod = value % 36
            if mod < 10:
                # ASCII值 0-9 是 48~57
                asc_list.insert(0, mod + 48)
            else:
                # ASCII值 A-Z 是 65~90，减去 0-9 的10后等于55
                asc_list.insert(0, mod + 55)
            value = value // 36
        result_str = ""
        for r in asc_list:
            result_str += chr(r)
        return result_str

    def update_text_decs(decs_list: list[MultiCodeServerKeyDecs]):
        """更新 key 的描述json文件

        Args:
            decs_list (list[ServerKeyDecs]): 更新的列表
        """
        if len(decs_list) == 0:
            return
        json_path = GitlabServeFileTool.server_text_key_desc_path()
        json_dic = {}
        if os.path.exists(json_path):
            with open(json_path, encoding="utf8") as f:
                json_str = f.read()
                json_dic = json.loads(json_str)
                f.close()
        with open(json_path, mode="w", encoding="utf8") as f:
            for decs in decs_list:
                json_dic[decs.key] = {
                    "module_name": decs.module_name,
                    "origin_key": decs.origin_key,
                }
            f.write(json.dumps(json_dic, indent=2, sort_keys=True, ensure_ascii=False))
            f.close()

    def update_res_decs(decs_list: list[MultiCodeServerKeyDecs]):
        """更新图片资源 key 的描述json文件

        Args:
            decs_list (list[ServerKeyDecs]): 更新的列表
        """
        if len(decs_list) == 0:
            return
        json_path = GitlabServeFileTool.server_res_key_desc_path()
        json_dic = {}
        if os.path.exists(json_path):
            with open(json_path, encoding="utf8") as f:
                json_str = f.read()
                json_dic = json.loads(json_str)
                f.close()
        with open(json_path, mode="w", encoding="utf8") as f:
            for decs in decs_list:
                json_dic[decs.key] = {
                    "module_name": decs.module_name,
                    "origin_key": decs.origin_key,
                }
            f.write(json.dumps(json_dic, indent=2, sort_keys=True, ensure_ascii=False))
            f.close()

    def update_useless(module_name: str, str_list: list[str]):
        """上传没有使用到的国际化字符串

        Args:
            module_name (str): 组件名
            str_list (list[str]): 没使用到的字符串数组
        """
        if len(str_list) == 0:
            return
        json_path = GitlabServeFileTool.server_key_useless_path()
        json_dic = {}
        if os.path.exists(json_path):
            with open(json_path, encoding="utf8") as f:
                json_str = f.read()
                json_dic = json.loads(json_str)
                f.close()
        with open(json_path, mode="w", encoding="utf8") as f:
            json_dic[module_name] = str_list
            f.write(json.dumps(json_dic, indent=2, sort_keys=True, ensure_ascii=False))
            f.close()

    def pull_form_server():
        """拉取服务端最新文件"""
        tdf_tools_path = os.path.expanduser("~") + "/" + FileUtil._I18N_PATH
        Cmd.run("git -C {} pull".format(tdf_tools_path))

    def upload_to_server():
        """上传文件到服务端"""
        tdf_tools_path = os.path.expanduser("~") + "/" + FileUtil._I18N_PATH
        Cmd.run("git -C {} add .".format(tdf_tools_path))
        Cmd.run("git -C {} commit -m 'update i8n'".format(tdf_tools_path))
        Cmd.run("git -C {} push".format(tdf_tools_path))

    def server_res_last_key_path() -> str:
        """获取服务端最新的key的本地地址

        Returns:
            _type_: 服务端最新的key的本地地址
        """
        tool_path = FileUtil.tdf_i18n_path()
        project_app: ProjectApp = WorkSpaceTool.get_project_app()
        project_type: ProjectType = WorkSpaceTool.get_project_type()
        if project_type == ProjectType.FLUTTER:
            return tool_path + "/flutter_res_last_server_key.txt"
        else:
            return tool_path + "/{}_res_last_server_key.txt".format(project_app.decs())

    def server_text_last_key_path() -> str:
        """获取服务端最新的key的本地地址

        Returns:
            _type_: 服务端最新的key的本地地址
        """
        tool_path = FileUtil.tdf_i18n_path()
        project_app: ProjectApp = WorkSpaceTool.get_project_app()
        project_type: ProjectType = WorkSpaceTool.get_project_type()
        if project_type == ProjectType.FLUTTER:
            return tool_path + "/flutter_text_last_server_key.txt"
        else:
            return tool_path + "/{}_text_last_server_key.txt".format(project_app.decs())

    def server_text_key_desc_path() -> str:
        """获取服务端文案映射关系的地址

        Returns:
            _type_: 获取服务端映射关系的地址
        """
        tool_path = FileUtil.tdf_i18n_path()
        project_app: ProjectApp = WorkSpaceTool.get_project_app()
        project_type: ProjectType = WorkSpaceTool.get_project_type()
        if project_type == ProjectType.FLUTTER:
            return tool_path + "/flutter_text_server_key.json"
        else:
            return tool_path + "/{}_text_server_key.json".format(project_app.decs())

    def server_res_key_desc_path() -> str:
        """获取服务端图片资源映射关系的地址

        Returns:
            _type_: 获取服务端映射关系的地址
        """
        tool_path = FileUtil.tdf_i18n_path()
        project_app: ProjectApp = WorkSpaceTool.get_project_app()
        project_type: ProjectType = WorkSpaceTool.get_project_type()
        if project_type == ProjectType.FLUTTER:
            return tool_path + "/flutter_res_server_key.json"
        else:
            return tool_path + "/{}_res_server_key.json".format(project_app.decs())

    def server_text_key_desc_json() -> dict:
        json_path = GitlabServeFileTool.server_text_key_desc_path()
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                json_data = f.read()
                json_dict = json.loads(json_data)
                return json_dict

    def server_key_useless_path() -> str:
        """获取服务端没用到的key的本地地址

        Returns:
            _type_: 本地没用到的key的本地地址，主要是%等转义符
        """
        tool_path = FileUtil.tdf_i18n_path()
        project_app: ProjectApp = WorkSpaceTool.get_project_app()
        project_type: ProjectType = WorkSpaceTool.get_project_type()
        if project_type == ProjectType.FLUTTER:
            return tool_path + "/flutter_useless_key.json"
        else:
            return tool_path + "/{}_useless_key.json".format(project_app.decs())

    def server_in_operation_path() -> str:
        """获取是否生成code的文件地址"""
        tool_path = FileUtil.tdf_i18n_path()
        project_app: ProjectApp = WorkSpaceTool.get_project_app()
        project_type: ProjectType = WorkSpaceTool.get_project_type()
        if project_type == ProjectType.FLUTTER:
            return tool_path + "/flutter_in_operation.text"
        else:
            return tool_path + "/{}_in_operation.text".format(project_app.decs())

    def write_res_excel(data: list[dict], sheet_name: str):
        """写入图片资源excel"""
        df = pd.DataFrame(data)
        GitlabServeFileTool._write_excel(
            df, sheet_name, GitlabServeFileTool.server_res_excel_path()
        )

    def write_text_excel(data: list[dict], sheet_name: str):
        """写入文案excel"""
        df = pd.DataFrame(data)
        GitlabServeFileTool._write_excel(
            df, sheet_name, GitlabServeFileTool.server_text_excel_path()
        )

    def _write_excel(df: pd.DataFrame, sheet_name: str, file_path: str):
        """写入excel"""
        if os.path.exists(file_path):
            # 保存到Excel
            with pd.ExcelWriter(
                file_path, mode="a", if_sheet_exists="replace"
            ) as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            # 保存到Excel
            with pd.ExcelWriter(file_path) as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    def server_res_excel_path() -> str:
        """获取服务端图片资源excel的地址"""
        tool_path = FileUtil.tdf_i18n_path()
        project_app: ProjectApp = WorkSpaceTool.get_project_app()
        project_type: ProjectType = WorkSpaceTool.get_project_type()
        if project_type == ProjectType.FLUTTER:
            return tool_path + "/flutter_res_excel.xlsx"
        else:
            return tool_path + "/{}_res_excel.xlsx".format(project_app.decs())

    def server_text_excel_path() -> str:
        """获取服务端文案excel的地址"""
        tool_path = FileUtil.tdf_i18n_path()
        project_app: ProjectApp = WorkSpaceTool.get_project_app()
        project_type: ProjectType = WorkSpaceTool.get_project_type()
        if project_type == ProjectType.FLUTTER:
            return tool_path + "/flutter_text_excel.xlsx"
        else:
            return tool_path + "/{}_text_excel.xlsx".format(project_app.decs())
