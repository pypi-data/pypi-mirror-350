import os

import requests
from funbuild.shell import run_shell_list
from funutil import getLogger

from .base import BaseInstall

logger = getLogger("funinstall")


class NewApiInstall(BaseInstall):
    def __init__(self, overwrite=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.overwrite = overwrite

    def get_download_url(self) -> dict[str, str]:
        url = "https://api.github.com/repos/QuantumNous/new-api/releases/latest"
        response = requests.get(url).json()
        return dict(
            (asset["name"], asset["browser_download_url"])
            for asset in response["assets"]
        )

    def _install(self, device="one-api", *args, **kwargs) -> bool:
        root = f"{os.environ.get('HOME')}/opt/new-api"
        if not os.path.exists(root):
            logger.info(f"目录{root}不存在，创建")
            os.makedirs(root, exist_ok=True)

        run_shell_list(
            [
                f"cd {root}",
                f"curl -L -o one-api {self.get_download_url()[device]}",
                "chmod u+x one-api",
            ]
        )
        return True

    def install_linux(self, *args, **kwargs) -> bool:
        return self._install("one-api", *args, **kwargs)

    def install_macos(self, *args, **kwargs) -> bool:
        return self._install("one-api-macos", *args, **kwargs)

    def install_windows(self, *args, **kwargs) -> bool:
        return self._install("one-api.exe", *args, **kwargs)
