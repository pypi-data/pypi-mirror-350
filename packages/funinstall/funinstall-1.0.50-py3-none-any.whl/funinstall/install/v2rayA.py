from funbuild.shell import run_shell
from funutil import getLogger

from .base import BaseInstall

logger = getLogger("funinstall")


class V2RayAInstall(BaseInstall):
    def __init__(self, version=None, lasted=False, update=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = version
        self.lasted = lasted
        self.update = update

    def install_macos(self, *args, **kwargs) -> bool:
        logger.info("添加 v2rayA 的 Tap")
        run_shell("brew tap v2raya/v2raya")
        logger.info("安装 v2rayA")
        run_shell("brew install v2raya/v2raya/v2raya")
        run_shell("brew services start v2raya")
        return True

    def install_linux(self, *args, **kwargs) -> bool:
        """
        https://v2raya.org/docs/prologue/installation/debian/
        """
        logger.info("添加源")
        run_shell(
            "wget -qO - https://apt.v2raya.org/key/public-key.asc | sudo tee /etc/apt/keyrings/v2raya.asc"
        )
        run_shell(
            'echo "deb [signed-by=/etc/apt/keyrings/v2raya.asc] https://apt.v2raya.org/ v2raya main" | sudo tee /etc/apt/sources.list.d/v2raya.list'
        )
        run_shell("sudo apt update")
        logger.info("安装")
        run_shell("sudo apt install v2raya v2ray")
        logger.info("设置开机自启动")
        run_shell("sudo systemctl enable v2raya.service")
        logger.info("启动")
        run_shell("sudo systemctl start v2raya.service")
        return True
