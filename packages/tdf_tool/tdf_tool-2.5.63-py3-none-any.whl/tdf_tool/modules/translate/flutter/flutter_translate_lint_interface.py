from abc import ABC, abstractmethod
from tdf_tool.modules.translate.flutter.flutter_tranalate_interface import (
    FlutterTranslateDartFileMixin,
    FlutterTranslateModuleMixin,
)


class FlutterTranslateLintInterface(
    ABC, FlutterTranslateDartFileMixin, FlutterTranslateModuleMixin
):
    @abstractmethod
    def lint_all(self):
        pass

    @abstractmethod
    def lint_module(self, name):
        pass

    @abstractmethod
    def lint_path(self, path):
        pass


# 单引号lint的结果类
class TranslateLintApostrophe:
    def __init__(self, file_path: str, apostrophe_strs: list[str]):
        # 单引号文件路径
        self.file_path = file_path
        # 单引号的字符串
        self.apostrophe_strs = apostrophe_strs
