from funbuild.shell import run_shell
from funutil import getLogger

from .base import BaseInstall

logger = getLogger("funinstall")


class UIFInstall(BaseInstall):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def install_linux(self, *args, **kwargs) -> bool:
        """
        https://ui4freedom.org/UIF_help/docs/install/linux

        cat /usr/bin/uif/uif_key.txt # Password
        cat /usr/bin/uif/uif_api_address.txt # API Address
        cat /usr/bin/uif/uif_web_address.txt # Web Address
        """
        run_shell(
            "curl -L -o funinstall_uif.sh https://fastly.jsdelivr.net/gh/UIforFreedom/UIF@master/uifd/linux_install.sh"
        )
        run_shell("chmod 755 ./funinstall_uif.sh")
        run_shell("sudo bash funinstall_uif.sh")
        run_shell("sudo systemctl enable ui4freedom")
        run_shell("sudo systemctl restart ui4freedom")

        logger.success("成功安装 UIF")
        run_shell("rm funinstall_uif.sh")
        return True
