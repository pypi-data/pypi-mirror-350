from .command import app as install_app
from .command import install_code_server, install_go, install_newapi, install_nodejs

__all__ = [
    "install_app",
    "install_go",
    "install_nodejs",
    "install_newapi",
    "install_code_server",
]
