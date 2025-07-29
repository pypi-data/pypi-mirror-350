from funbuild.shell import run_shell
from funutil import getLogger

from .base import BaseInstall

logger = getLogger("funinstall")


class NodeJSInstall(BaseInstall):
    def __init__(self, version=None, lasted=False, update=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = version
        self.lasted = lasted
        self.update = update

    def install_macos(self, *args, **kwargs) -> bool:
        run_shell("brew install nodejs")
        return True

    def install_linux(self, *args, **kwargs) -> bool:
        """
        使用一键脚本安装new-api
        https://docs.newapi.pro/installation/local-development/#_6
        """
        """
            使用一键脚本安装nodeJs
            https://github.com/Jrohy/nodejs-install
            """
        run_shell(
            "curl -L -o funinstall_nodejs.sh https://nodejs-install.netlify.app/install.sh"
        )
        if self.version:
            run_shell(f'sudo bash funinstall_nodejs.sh -v {self.version}"')
            logger.success(f"成功安装 nodeJs {self.version}")
        elif self.lasted:
            run_shell("sudo bash funinstall_nodejs.sh -l")
            logger.success("成功安装 nodeJs")
        elif self.update:
            run_shell("sudo bash funinstall_nodejs.sh -f")
            logger.success("成功更新 nodeJs")
        else:
            run_shell("sudo bash funinstall_nodejs.sh")
            logger.success("成功安装 nodeJs")
        run_shell("rm funinstall_nodejs.sh")
        return True
