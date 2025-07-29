import typer
from funutil import getLogger

from .brew import BrewInstall
from .code_server import CodeServerInstall
from .frpc import FrpcInstall
from .go import GoInstall
from .newapi import NewApiInstall
from .nodejs import NodeJSInstall
from .onehub import OnehubInstall
from .uif import UIFInstall
from .v2rayA import V2RayAInstall

logger = getLogger("funinstall")

app = typer.Typer()


@app.command(name="code-server")
def install_code_server() -> bool:
    return CodeServerInstall().install()


@app.command(name="go")
def install_go(
    version: str = typer.Option(None, "--version", "-v", help="Go 版本"),
) -> bool:
    return GoInstall(version=version).install()


@app.command(name="new-api")
def install_newapi() -> bool:
    return NewApiInstall().install()


@app.command(name="nodejs")
def install_nodejs(
    version: str = typer.Option(None, "--version", "-v", help="nodejs 版本"),
    lasted: bool = typer.Option(False, "--lasted", "-l", help="是否安装最新版本"),
    update: bool = typer.Option(False, "--update", "-u", help="是否更新版本"),
) -> bool:
    return NodeJSInstall(version=version, lasted=lasted, update=update).install()


@app.command(name="brew")
def install_brew(*args, **kwargs) -> bool:
    return BrewInstall().install()


@app.command(name="v2rayA")
def install_v2rayA():
    return V2RayAInstall().install()


@app.command(name="frpc")
def install_frpc():
    return FrpcInstall().install()


@app.command(name="uif")
def install_uif():
    return UIFInstall().install()


@app.command(name="onehub")
def install_onehub():
    return OnehubInstall().install()
