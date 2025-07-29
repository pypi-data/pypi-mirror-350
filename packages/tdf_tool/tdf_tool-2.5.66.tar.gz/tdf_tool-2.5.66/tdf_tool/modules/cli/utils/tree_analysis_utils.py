
import os, json, subprocess


class TreeAnalysisUtils:
    
    command = "flutter pub deps --json"
    
    def __init__(self, name, path):
        self.name = name # 依赖树顶层节点名称
        self.path = path # 依赖树顶层节点目录
        
        try:
            result = subprocess.run(
                ["flutter", "pub",  "deps",  "--json"],
                cwd=self.path,
                capture_output=True,
                text=True
            )
            config = json.loads(result.stdout)
            self.packagesConfig = config['packages']
            self.rootConfig = next((item for item in self.packagesConfig if item.get("name", "") == self.name), None)
            if self.rootConfig is None:
                print(f"An error occurred: can't find own")
                exit(-1)
            print("tree init complete")
        except Exception as e:
            print(f"An error occurred: {e}")
            exit(-1)
    
    # parentModuleName模块中 是否 直接依赖childModuleName
    def existDirectDependency(self, parentModuleName: str, childModuleName) -> bool:
        parentModuleConfig = next((item for item in self.packagesConfig if item.get("name", "") == parentModuleName), None)
        if parentModuleConfig:
            parentModuleDependencis = parentModuleConfig['dependencies']
            result = next((item for item in parentModuleDependencis if item == childModuleName), None)
            print('Analysis direct dependency:  <{0}> in <{1}>'.format(childModuleName, parentModuleName))
            print('result：{0}'.format(result != None))
            if result:
                return True            
        return False
            
        
    # 模块是当前模块直接/间接依赖的
    def existDependency(self, parentModuleName: str, childModuleName) -> bool:
        print("Analysis in-direct dependency: <{0}> in <{1}>".format(childModuleName, parentModuleName))  
        result = self.__dfsInitAndStart(parentModuleName, childModuleName)
        print('result：{0}'.format(result))
        return result

    def __dfsInitAndStart(self, parentModuleName: str, childModuleName) -> bool:
        self.hasDfsList = []
        return self.__dfsFindModule(parentModuleName, childModuleName)

    def __dfsFindModule(self, parentModuleName: str, childModuleName) -> bool:
        if parentModuleName in self.hasDfsList:
            return False
        self.hasDfsList.append(parentModuleName) # 记录已遍历过的模块，优化遍历速度
        
        moduleConfig = next((item for item in self.packagesConfig if item.get("name", "") == parentModuleName), None)
        if moduleConfig:
            moduleDependencies = moduleConfig["dependencies"]
            if isinstance(moduleDependencies, list):
                if childModuleName in moduleDependencies:
                    return True
                else:
                    for dependency in moduleDependencies:
                        if self.__dfsFindModule(dependency, childModuleName):
                            return True
        return False