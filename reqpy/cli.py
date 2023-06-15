"""This module provides the reqpy CLI."""

from typing import Optional

import typer
from typing_extensions import Annotated

from reqpy import __app_name__, __version__

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()
def _sco_callback(value:bool) -> None:
    if value:
        print('allez le sco!!')
        raise typer.Exit()


@app.command(short_help='hello world')
def hello(name: str,
    lastname: Annotated[str, typer.Option(help="Last name of person to greet.")] = "",
    formal: Annotated[bool, typer.Option(help="Say hi formally.")] = False,
):
    """
    Say hi to NAME, optionally with a --lastname.

    If --formal is used, say hi very formally.
    """
    if formal:
        print(f"Good day Ms. {name} {lastname}.")
    else:
        print(f"Hello {name} {lastname}")


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
