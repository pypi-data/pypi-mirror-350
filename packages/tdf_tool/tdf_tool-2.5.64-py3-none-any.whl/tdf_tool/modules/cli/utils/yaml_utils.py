import os
from ruamel import yaml

from tdf_tool.tools.print import Print


# yaml 文件操作
class YamlFileUtils:
    yamlFileName = "pubspec.yaml"
    overridesYamlFileName = "pubspec_overrides.yaml"
    dependenciesNode = "dependencies"
    dependencyOverridesNode = "dependency_overrides"

    def __init__(self, path):
        self.yamlPath = os.path.join(path, YamlFileUtils.yamlFileName)
        self.overridesYamlPath = os.path.join(path, YamlFileUtils.overridesYamlFileName)

    def readOverrideDepsKeys(self) -> list[str]:
        if not os.path.exists(self.overridesYamlPath):
            return []
        with open(self.overridesYamlPath, encoding="utf-8") as f:
            doc = yaml.round_trip_load(f)
            node = YamlFileUtils.dependencyOverridesNode
            if (
                isinstance(doc, dict)
                and doc.__contains__(node)
                and isinstance(doc[node], dict)
            ):
                return list(dict(doc[node]).keys())
        return []

    def writeOverrideDepsByDict(self, deps: list[dict], isShell: bool = True):
        # 清空pubspec.yaml中的overrides
        self.__clear_yaml_overrides()
        if not os.path.exists(self.overridesYamlPath):
            with open(self.overridesYamlPath, "w", encoding="utf-8") as f:
                f.close()
        # 写入到pubspec_overrides.yaml文件中
        with open(self.overridesYamlPath, encoding="utf-8") as f:
            doc = yaml.round_trip_load(f)
            if doc is None:
                doc = {}
            node = YamlFileUtils.dependencyOverridesNode
            if isinstance(doc, dict):
                if doc.__contains__(node) and doc[node] is not None:
                    doc[node] = None

            # 重写依赖
            overrideDict = {}
            for item in deps:
                key = list(item.keys())[0]
                overrideDict[key] = item[key]
            if len(deps) > 0:
                doc[node] = overrideDict
            f.close()
            with open(self.overridesYamlPath, "w", encoding="utf-8") as rf:
                yaml.round_trip_dump(
                    doc,
                    rf,
                    default_flow_style=False,
                    encoding="utf-8",
                    allow_unicode=True,
                )
                rf.close()

    # 清空yaml文件中的dependency_overrides 节点
    def __clear_yaml_overrides(self):
        with open(self.yamlPath, encoding="utf-8") as f:
            doc = yaml.round_trip_load(f)
            node = YamlFileUtils.dependencyOverridesNode
            if isinstance(doc, dict):
                if doc.__contains__(node) and doc[node] is not None:
                    del doc[node]
            with open(self.yamlPath, "w+", encoding="utf-8") as reW:
                yaml.round_trip_dump(
                    doc,
                    reW,
                    default_flow_style=False,
                    encoding="utf-8",
                    allow_unicode=True,
                )
                reW.close()
            f.close()
