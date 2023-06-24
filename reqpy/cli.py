"""This module provides the reqpy CLI."""

from typing import Optional

import typer
from typing_extensions import Annotated

from reqpy import __app_name__, __version__
import reqpy

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()
def _sco_callback(value:bool) -> None:
    if value:
        print('allez le sco!!')
        raise typer.Exit()


@app.command(short_help='delete the existing requirement database')
def delete():
    reqpy.reset_reqpy()

@app.callback()
def common(
    clx : typer.Context,
    version:bool= typer.Option(
        None, "--version",'-v',
        callback=_version_callback,
        help="Provide version of the package"
    ),
    sco:bool= typer.Option(
        None, "--sco",'-sco',
        callback=_sco_callback,
        help="Provide sco message"
    ),
):
   pass
#     version: Optional[bool] = typer.Option(
#         None,
#         "--version",
#         "-v",
#         help="Show the application's version and exit.",
#         callback=_version_callback,
#         is_eager=True,
#     )
# ) -> None:
#     return
