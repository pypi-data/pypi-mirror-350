import json
import os
import subprocess
from ruamel import yaml
from typing import Tuple
from tdf_tool.tools.print import Print
from tdf_tool.tools.shell_dir import ShellDir


class InitialJsonConfig:

    def __init__(self):
        config = self.__getInitialConfig()
        self.featureBranch = config[0]
        self.shellName = config[1]
        self.moduleNameList = config[2]
        self.forceOverrides = self.__getDepsEnhancement()

    # 获取当前分支
    def get_current_branch(self):
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True
        )
        return result.stdout.strip()

    def get_project_name(self):
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

    # 获取环境配置文件
    def __getInitialConfig(self) -> Tuple:
        ShellDir.goInShellDir()
        if os.path.exists("tdf_cache") is not True:
            Print.error("读取项目环境配置文件initial_config.json失败")

        currentFeatureBranch = self.get_current_branch()
        shellName = self.get_project_name()

        jsonData = dict
        with open("./tdf_cache/initial_config.json", "r", encoding="utf-8") as rf:
            jsonData = json.loads(rf.read())
            rf.close()
            if isinstance(jsonData, dict) and jsonData.__contains__("moduleNameList"):
                return (
                    currentFeatureBranch,
                    shellName,
                    jsonData["moduleNameList"],
                )
            else:
                Print.error("读取项目环境配置文件initial_config.json失败")

    def __getDepsEnhancement(self):
        forceOverrides: list = []
        with open("./tdf_cache/depsEnhancement.json", "r", encoding="utf-8") as rf:
            jsonData = json.loads(rf.read())
            if isinstance(jsonData, dict) and jsonData.__contains__("forceOverrides"):
                overrideJson = jsonData["forceOverrides"]
                if isinstance(overrideJson, dict):
                    print(overrideJson)
                    forceOverrides = [
                        {item: overrideJson[item]} for item in overrideJson
                    ]
        return forceOverrides

    def clear_deps_enhancement(self):
        with open("./tdf_cache/initial_config.json", encoding="utf-8") as f:
            jsonData = json.loads(f.read())
            if jsonData.__contains__("depsEnhancement"):
                del jsonData["depsEnhancement"]
            if jsonData.__contains__("shellName"):
                del jsonData["shellName"]
            if jsonData.__contains__("featureBranch"):
                del jsonData["featureBranch"]
            f.close()
            with open("./tdf_cache/initial_config.json", "w", encoding="utf-8") as rf:
                rf.write(json.dumps(jsonData, ensure_ascii=False, indent=4))
                rf.close()
