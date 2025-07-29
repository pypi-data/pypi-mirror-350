from funbuild.shell import run_shell
from funutil import getLogger

from .base import BaseInstall

logger = getLogger("funinstall")


class FrpcInstall(BaseInstall):
    def __init__(self, version: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = version

    def install_linux(self, *args, **kwargs) -> bool:
        """
        https://github.com/farfarfun/funfrp/tree/master/src/funfrp/frpc
        """
        run_shell(
            "curl -L -o funinstall_frpc.sh https://raw.githubusercontent.com/stilleshan/frpc/master/frpc_linux_install.sh"
        )
        run_shell("chmod +x funinstall_frpc.sh")
        run_shell("sudo bash funinstall_frpc.sh")
        run_shell("rm funinstall_frpc.sh")
        return True

    def uninstall_linux(self, *args, **kwargs) -> bool:
        run_shell(
            "curl -L -o funinstall_frpc.sh https://raw.githubusercontent.com/stilleshan/frpc/master/frpc_linux_uninstall.sh"
        )
        run_shell("chmod +x funinstall_frpc.sh")
        run_shell("sudo bash funinstall_frpc.sh")
        run_shell("rm funinstall_frpc.sh")
        return True
