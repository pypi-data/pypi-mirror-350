
import os


class Token:
    """
    git private token 配置
    """
    def init(self):
        git_private_token = input(
            "请输入 git_private_token："
        )
        tdf_tool_config_path = os.path.join(os.path.expanduser("~"), ".tdf_tool_config")
        with open(tdf_tool_config_path, "w", encoding="utf-8") as f:
            f.write("git_private_token={0}".format(git_private_token))
            f.close()
            
        Print.line("token已配置")
        print()