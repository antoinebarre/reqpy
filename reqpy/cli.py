"""This module provides the reqpy CLI."""

import typer
from reqpy import __app_name__, __version__
import reqpy
from pathlib import Path

# initiate CLI
app = typer.Typer(add_completion=False)


@app.command(
        short_help="Provide an analysis on the console of the reqpy database",
        )
def validate():
    res = reqpy.validate_reqpy_database(
        mainPath=Path(),
        show_console=True
    )
    raise typer.Exit(code=not res)


@app.command(
        short_help=(
            'delete the existing requirement database'
            ' and create an empty database'
        )
    )
def reset():
    reqpy.reset_reqpy()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def common(
    clx: typer.Context,
    version: bool = typer.Option(
        None, "--version", '-v',
        callback=_version_callback,
        help="Provide version of the package"
    ),
):
    pass
