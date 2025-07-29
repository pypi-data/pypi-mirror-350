from abc import ABCMeta, abstractmethod
from enum import Enum
from googletrans import Translator
import requests
import random
from hashlib import md5
from tdf_tool.tools.print import Print

MULTI_CODE_KEY = "zh_code"
MULTI_MAF_KEY = "MULTI_MAF"
MULTI_MIF_KEY = "MULTI_MIF"


class LanguageType(Enum):
    en_US = 1  # 英文
    th_TH = 2  # 泰语
    zh_CN = 3  # 简体中文
    zh_TW = 4  # 繁体中文
    es_ES = 5  # 西班牙语
    it_IT = 6  # 意大利
    de_DE = 7  # 德语
    ja_JP = 8  # 日语
    ru_RU = 9  # 俄语
    pt_BR = 10  # 葡萄牙语
    fr_FR = 11  # 法语
    ko_KR = 12  # 韩语
    # 第一步：新增枚举

    @staticmethod
    def all():
        return list(LanguageType.ios_lang_map().keys())

    @staticmethod
    def ios_lang_map() -> dict:
        return {
            LanguageType.zh_CN: "zh-Hans",
            LanguageType.zh_TW: "zh-Hant",
            LanguageType.en_US: "en",
            LanguageType.th_TH: "th",
            LanguageType.es_ES: "es",
            LanguageType.it_IT: "it",
            LanguageType.de_DE: "de",
            LanguageType.ja_JP: "ja",
            LanguageType.ru_RU: "ru",
            LanguageType.pt_BR: "pt-BR",
            LanguageType.fr_FR: "fr",
            LanguageType.ko_KR: "ko",
            # 第二步：补全iOS对应的语言
        }

    @staticmethod
    def text_dart_file(module_name, class_name):
        # 生成所有语言的导入
        imports = "import 'package:{0}/tdf_intl/i18n.dart';\n".format(module_name)
        for i in LanguageType.all():
            imports += "import 'package:{0}/tdf_intl/i18n/{0}_{1}.dart';\n".format(
                module_name, i.str()
            )
        # 生成所有语言的map
        i18nMap = ""
        for i in LanguageType.all():
            i18nMap += "i18nMap!['{0}'] = {0}Map;\n          ".format(i.str())
        # 文件模版
        return """
{imports}
// ignore: implementation_imports
import 'package:tdf_language/tdf_language.dart';

class {1}I18n {{

  static Map<String, Map<String, String>>? i18nMap;
  static Map<String, Map<String, String>> getInstance() {{
      if (i18nMap == null) {{
          i18nMap = Map();
          {i18nMap}
      }}
      return i18nMap!;
  }}
}}

extension {1}IntlStringExtension on String {{
  String get intl {{
    return TDFLanguage.intl(
      input: this,
      i18nMap: {1}I18n.getInstance(),
      zhChCodeMap: zh_codeMap,
    );
  }}
}}
""".format(
            module_name,
            class_name,
            imports=imports,
            i18nMap=i18nMap,
        )

    @staticmethod
    def res_dart_file(module_name, class_name):
        # 生成所有语言的导入
        imports = "import 'package:{0}/tdf_res_intl/res_i18n.dart';\n".format(
            module_name
        )
        for i in LanguageType.all():
            imports += (
                "import 'package:{0}/tdf_res_intl/res_i18n/{0}_{1}.dart';\n".format(
                    module_name, i.str()
                )
            )
        # 生成所有语言的map
        i18nMap = ""
        for i in LanguageType.all():
            i18nMap += "i18nMap!['{0}'] = {0}Map;\n          ".format(i.str())
        # 文件模版
        return """
{imports}
// ignore: implementation_imports
import 'package:tdf_language/tdf_language.dart';

class {1}I18n {{

  static Map<String, Map<String, String>>? i18nMap;
  static Map<String, Map<String, String>> getInstance() {{
      if (i18nMap == null) {{
          i18nMap = Map();
          {i18nMap}
      }}
      return i18nMap!;
  }}
}}

extension {1}ResIntlStringExtension on String {{
  String get resIntl {{
    return TDFLanguage.resIntl(
      input: this,
      i18nMap: {1}I18n.getInstance(),
      zhChCodeMap: zh_codeMap,
    );
  }}
}}
""".format(
            module_name,
            class_name,
            imports=imports,
            i18nMap=i18nMap,
        )

    def init(string_type: str):
        lang_map = LanguageType.ios_lang_map()
        # lang_map反转
        lang_map_reverse = {v: k for k, v in lang_map.items()}
        return lang_map_reverse[string_type]

    def baidu(self) -> str:
        lang_map = {
            LanguageType.en_US: "en",
            LanguageType.th_TH: "th",
            LanguageType.zh_CN: "zh",
            LanguageType.zh_TW: "cht",
            LanguageType.es_ES: "spa",
            LanguageType.it_IT: "it",
            LanguageType.de_DE: "de",
            LanguageType.ja_JP: "jp",
            LanguageType.ru_RU: "ru",
            LanguageType.pt_BR: "pt",
            LanguageType.fr_FR: "fra",
            LanguageType.ko_KR: "kor",
            # 第三步：补全百度对应的code
        }
        if self in lang_map:
            return lang_map[self]
        raise ValueError(f"Unsupported language type: {self}")

    def google(self) -> str:
        lang_map = {
            LanguageType.en_US: "en",
            LanguageType.th_TH: "th",
            LanguageType.zh_CN: "zh-CN",
            LanguageType.zh_TW: "zh-TW",
            LanguageType.es_ES: "es",
            LanguageType.it_IT: "it",
            LanguageType.de_DE: "de",
            LanguageType.ja_JP: "ja",
            LanguageType.ru_RU: "ru",
            LanguageType.pt_BR: "pt",
            LanguageType.fr_FR: "fr",
            LanguageType.ko_KR: "ko",
            # 第三步：补全谷歌对应的code
        }
        if self in lang_map:
            return lang_map[self]
        raise ValueError(f"Unsupported language type: {self}")

    def str(self) -> str:
        return self.name

    def ios_str(self) -> str:
        lang_map = LanguageType.ios_lang_map()
        return lang_map[self]


class TranslateType(Enum):
    BAIDU = 1  # 百度翻译，百度翻译 %d \n 这类符号翻译出来有问题，还是使用谷歌翻译比较好
    GOOGLE = 2  # 谷歌翻译


class Translate(metaclass=ABCMeta):
    @abstractmethod
    def translate(
        self, text: str, dest=LanguageType.en_US, src=LanguageType.zh_CN
    ) -> str:
        pass


class TranslateTool(Translate):
    def __init__(self):
        # 谷歌翻译，带%占位符的使用谷歌翻译
        self.__google__translator = self.__generate_translate(TranslateType.GOOGLE)
        # 剩余其他的文案使用百度翻译
        self.__baidu_translator = self.__generate_translate(TranslateType.BAIDU)

    def translate(
        self,
        text: str,
        dest=LanguageType.en_US,
        src=LanguageType.zh_CN,
    ) -> str:
        if src == dest:
            return text
        has_double_quotes = False
        # 翻译前去掉 前后双引号
        if text.startswith('"') and text.endswith('"'):
            has_double_quotes = True
            text = text[1:-1]
        if dest == LanguageType.en_US or dest == LanguageType.th_TH:
            # 处理 《》【】“”，因为这些在外语会翻译成双引号，需要加转义符
            text = text.replace("《", r"\"")
            text = text.replace("》", r"\"")
            text = text.replace("【", r"\"")
            text = text.replace("】", r"\"")
            text = text.replace("“", r"\"")
            text = text.replace("”", r"\"")
            text = text.replace("＂", r"\"")
        retry_count = 4
        # 翻译后的字符
        res_text = text
        while retry_count > 0:
            if "%" in text:
                # 带%占位符的只能使用谷歌翻译
                Print.title("开始谷歌翻译第{0}次：{1}".format(5 - retry_count, text))
                res_text = self.__google__translator.translate(text, src=src, dest=dest)
                Print.step("谷歌翻译第{0}次结果：{1}".format(5 - retry_count, res_text))
            else:
                if retry_count > 2:
                    # 先google翻译两次
                    Print.title(
                        "开始谷歌翻译第{0}次：{1}".format(5 - retry_count, text)
                    )
                    res_text = self.__google__translator.translate(
                        text, src=src, dest=dest
                    )
                    Print.step(
                        "谷歌翻译第{0}次结果：{1}".format(5 - retry_count, res_text)
                    )
                else:
                    # 重试次数小于3次，使用谷歌翻译
                    Print.title(
                        "开始百度翻译第{0}次：{1}".format(5 - retry_count, text)
                    )
                    res_text = self.__baidu_translator.translate(
                        text, src=src, dest=dest
                    )
                    Print.step(
                        "百度翻译第{0}次结果：{1}".format(5 - retry_count, res_text)
                    )
            if len(res_text) > 0:
                break
            retry_count -= 1
        # 偶尔会出现 \" 翻译成 \ "，需要检查替换一下
        res_text = res_text.replace('\ "', '\\"')
        if has_double_quotes:
            # 翻译完再加上 前后双引号
            res_text = '"' + res_text + '"'
        return res_text

    def __generate_translate(self, type) -> Translate:
        if type == TranslateType.BAIDU:
            return BaiduTranslate()
        else:
            return GoogleTranslate()


class BaiduTranslate(Translate):

    __appid = "20220505001202987"
    __appKey = "qmWBUEi75he1iVZQgqPg"
    __endpoint = "http://api.fanyi.baidu.com"
    __path = "/api/trans/vip/translate"
    __url = __endpoint + __path

    def translate(
        self, text: str, dest=LanguageType.en_US, src=LanguageType.zh_CN
    ) -> str:
        try:
            salt = random.randint(32768, 65536)
            sign = self.__make_md5(self.__appid + text + str(salt) + self.__appKey)

            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            payload = {
                "appid": self.__appid,
                "q": text,
                "from": src.baidu(),
                "to": dest.baidu(),
                "salt": salt,
                "sign": sign,
            }

            r = requests.post(self.__url, params=payload, headers=headers)
            result: dict = r.json()
            error_code = result.get("error_code")
            if error_code != None:
                error_msg = result.get("error_msg")
                Print.error(
                    "{0}百度翻译失败, error_code：{1}，error_msg：{2}".format(
                        text, error_code, error_msg
                    )
                )
            trans_result: list[dict] = result["trans_result"]
            return trans_result[0]["dst"]
        except Exception as e:
            Print.warning("{0} 百度翻译失败：{1}".format(text, e))
            # 空字符串, 代表翻译失败
            return ""

    def __make_md5(self, s: str, encoding="utf-8"):
        return md5(s.encode(encoding)).hexdigest()


class GoogleTranslate(Translate):
    def translate(
        self, text: str, dest=LanguageType.en_US, src=LanguageType.zh_CN
    ) -> str:
        try:
            translator = Translator()
            result_text = translator.translate(
                text, src=src.google(), dest=dest.google()
            ).text
            if result_text == text and dest != LanguageType.zh_TW:
                Print.warning("{0} google翻译失败, 查看是否有开启代理".format(text))
                # 空字符串, 代表翻译失败
                return ""
            else:
                return result_text
        except Exception as e:
            Print.warning("{0} google翻译失败, 查看是否有开启代理：{1}".format(text, e))
            # 空字符串, 代表翻译失败
            return ""
