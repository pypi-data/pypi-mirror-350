from funbuild.shell import run_shell
from funutil import getLogger

from .base import BaseInstall

logger = getLogger("funinstall")


class CodeServerInstall(BaseInstall):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def install_linux(self, *args, **kwargs) -> bool:
        """
        使用一键脚本安装code-server
        https://github.com/coder/code-server
        """
        run_shell("curl -L -o funinstall_cs.sh https://code-server.dev/install.sh")
        run_shell("sudo bash funinstall_cs.sh")
        logger.success("成功安装 code-server")
        run_shell("rm funinstall_cs.sh")
        return True
