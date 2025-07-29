import typer

from .install import install_app

app = typer.Typer()
app.add_typer(install_app, name="install")


def funinstall():
    app()
