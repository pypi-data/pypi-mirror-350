from funbuild.shell import run_shell
from funutil import getLogger

from .base import BaseInstall

logger = getLogger("funinstall")


class BrewInstall(BaseInstall):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def install_linux(self, *args, **kwargs) -> bool:
        return False

    def install_macos(self, *args, **kwargs) -> bool:
        """
        使用一键脚本安装go
        https://github.com/Jrohy/go-install
        """
        run_shell(
            "curl -L -o funinstall_brew.sh https://gitee.com/ineo6/homebrew-install/raw/master/install.sh"
        )
        run_shell("sudo bash funinstall_brew.sh")
        logger.success("成功安装 brew")
        run_shell("rm funinstall_brew.sh")
        return True
