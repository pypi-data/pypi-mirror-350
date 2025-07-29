import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional



DART_TEMPLATE = """import 'package:tdf_language/tdf_language.dart';

extension AssetsIntlExtension on String {{
  String get sourceIntl {{
    String code = TDFLanguage.getLanguage();
    List<String> pathList = this.split('.');
    if (pathList.length < 2) return this;
    
    String pre = pathList[0];
    if (pre.contains('-')) {{
      List<String> preList = pre.split('-');
      if (preList.length == 2) {{
        pre = preList[0];  // 移除已有语言后缀
      }}
    }}
    
    // 生成国际化路径
    final languagePath = '${{pre}}-$code.${{pathList[1]}}';
    return AssetsManager.sources.contains(languagePath) ? languagePath : this;
  }}
}}

class AssetsManager {{
  static List<String> sources = [
{}
  ];
}}
"""
class GenerateAsset:
    def __generateAssetsManager(self, package_dir: str):
        """生成资源管理文件到指定包目录"""
        package_path = Path(package_dir).resolve()
        assets_dir = package_path / "assets"
        output_path = package_path / "lib/gen/assets_intl.dart"

        if not assets_dir.exists():
            raise FileNotFoundError(f"资源目录不存在: {assets_dir}")

        # 收集资源路径
        asset_paths = set()
        for file_path in assets_dir.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                rel_path = file_path.relative_to(package_path)
                formatted = f"{rel_path.as_posix()}"
                asset_paths.add(formatted)

        # 生成代码
        indent = ' ' * 4
        path_list = ',\n'.join([f"{indent * 3}'{p}'" for p in sorted(asset_paths)])
        dart_code = DART_TEMPLATE.format(path_list)

        # 确保输出目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(dart_code)

        print(f"✅ 资源文件生成成功：{output_path}")

    def __handleAssetsIntl(self,package_dir: str):
        """处理自动生成文件"""
        gen_file = Path(package_dir) / "lib/gen/assets.gen.dart"
        if not gen_file.exists():
            raise FileNotFoundError(f"未找到生成文件: {gen_file}")

        with open(gen_file, 'r+', encoding='utf-8') as f:
            content = f.read()

            # 分步骤替换关键位置
            replacements = [            
                # 1. 替换image方法中的 _assetName
                (r'(Image\.asset\s*\([^)]*?)\b(_assetName)\b', r'\1\2.sourceIntl'),
                
                # 2. 替换provider方法中的 _assetName
                (r'(AssetImage\s*\([^)]*?)\b(_assetName)\b', r'\1\2.sourceIntl'),
                
                # 3. 替换path getter
                (r'(String get path =>\s*)\b(_assetName)\b', r'\1\2.sourceIntl')
            ]

            new_content = content
            modified = False
            for pattern, repl in replacements:
                new_content, n = re.subn(pattern, repl, new_content, flags=re.DOTALL)
                if n > 0:
                    modified = True

            # 添加导入语句
            if 'assets_intl.dart' not in new_content:
                new_content = new_content.replace(
                    '// coverage:ignore-file',
                    '// coverage:ignore-file\n'
                    'import \'assets_intl.dart\';\n',  # 使用相对路径导入
                    1
                )
                modified = True

            if modified:
                f.seek(0)
                f.write(new_content)
                f.truncate()
                print(f"✅ 成功更新 {gen_file}")
            else:
                print("⏩ 未发现需要修改的内容")

    def __runFlutterGen(self,package_dir: str):
        """执行Flutter资源生成"""
        pubspec_path = Path(package_dir) / "pubspec.yaml"
        if not pubspec_path.exists():
            raise FileNotFoundError(f"pubspec.yaml不存在于: {pubspec_path}")

        try:
            subprocess.run(
                ["fluttergen", "-c", str(pubspec_path)],
                check=True,
                stdout=subprocess.PIPE
            )
            print("✅ Fluttergen执行成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ Fluttergen执行失败: {e.stderr.decode()}")
            sys.exit(1)
    def fullProcess(self, package_dir: str):
        """完整工作流"""
        print(f"🏗️ 正在处理项目目录: {package_dir}")
        
        try:
            print("\n🔧 步骤1/3 执行Fluttergen资源生成")
            self.__runFlutterGen(package_dir)
            
            print("\n🔧 步骤2/3 生成国际化资源管理器")
            self.__generateAssetsManager(package_dir)
            
            print("\n🔧 步骤3/3 更新资源引用")
            self.__handleAssetsIntl(package_dir)
            
            print("\n🎉 所有流程完成！执行建议：")
            print("1. 检查生成文件: lib/gen/ 目录")
            print("2. 运行 dart format ./lib/gen")
        except Exception as e:
            print(f"\n❌ 流程中断: {str(e)}")
            sys.exit(1)