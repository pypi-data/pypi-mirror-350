import os
import json
import subprocess
from ruamel import yaml
from tdf_tool.tools.print import Print
from tdf_tool.tools.shell_dir import ShellDir


class ModuleTools:
    # 获取项目初始化数据
    def getInitJsonData() -> dict:

        ShellDir.goInShellDir()
        currentPath = os.getcwd()
        currentFeatureBranch = ModuleTools.get_current_branch()
        shellName = ModuleTools.get_project_name()
        with open("./tdf_cache/initial_config.json", "r", encoding="utf-8") as readF:
            fileData = readF.read()
            readF.close()
            data = json.loads(fileData)
            data["featureBranch"] = currentFeatureBranch
            data["shellName"] = shellName
            return data

    def getModuleNameList():
        initJsonData = ModuleTools.getInitJsonData()
        if initJsonData.__contains__("moduleNameList") and isinstance(
            initJsonData["moduleNameList"], list
        ):
            moduleNameList = initJsonData["moduleNameList"]
            return moduleNameList
        else:
            Print.error("❌ 请配置moduleNameList的值,以数组形式")

    def getModuleJsonData():  # 获取模块 git相关配置信息
        ShellDir.goTdfCacheDir()
        with open("module_config.json", "r", encoding="utf-8") as readF:
            fileData = readF.read()
            readF.close()
            return json.loads(fileData)

        # 获取当前分支

    def get_current_branch():
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True
        )
        return result.stdout.strip()

    def get_project_name():
        with open("pubspec.yaml", encoding="utf-8") as f:
            doc = yaml.round_trip_load(f)
            node = "name"
            if (
                isinstance(doc, dict)
                and doc.__contains__(node)
                and isinstance(doc[node], str)
            ):
                return doc[node]
        return None
