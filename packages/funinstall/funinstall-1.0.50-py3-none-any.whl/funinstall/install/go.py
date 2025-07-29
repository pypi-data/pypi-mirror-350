from funbuild.shell import run_shell
from funutil import getLogger

from .base import BaseInstall

logger = getLogger("funinstall")


class GoInstall(BaseInstall):
    def __init__(self, version: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = version

    def install_macos(self, *args, **kwargs) -> bool:
        run_shell("brew install go")
        return True

    def install_linux(self, *args, **kwargs) -> bool:
        """
        使用一键脚本安装go
        https://github.com/Jrohy/go-install
        """
        run_shell(
            "curl -L -o funinstall_go.sh https://go-install.netlify.app/install.sh"
        )
        if self.version:
            run_shell(f'sudo bash funinstall_go.sh -v {self.version}"')
            logger.success(f"成功安装 Go {self.version}")
        else:
            run_shell("sudo bash funinstall_go.sh")
            logger.success("成功安装 Go")
        run_shell("rm funinstall_go.sh")
        run_shell("sudo ln -fs /usr/local/go/bin/go /usr/local/bin/go")
        return True
