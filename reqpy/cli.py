"""This module provides the reqpy CLI."""

import os
import sys
import typer
from reqpy import __app_name__, __version__
import reqpy
from pathlib import Path
import click


PYTHON_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}"

PKG_DIR = os.path.dirname(os.path.abspath(__file__))


@click.group(
        context_settings=dict(help_option_names=['-h', '--help'],
                              max_content_width=120))
@click.version_option(
    __version__,
    '-V',
    '--version',
    message=f'%(prog)s, version %(version)s from { PKG_DIR } (Python { PYTHON_VERSION })',
)
def cli():
    """
    reqpy - Requirements Management Tools based on YAML
    """




# # initiate CLI
# app = typer.Typer(add_completion=True)

# @app.command(
#         short_help=(
#             'Create a fake requirement DataBase'
#         )
#     )
# def fake(
#     filePath: Path = typer.Option(
#         default=Path(),
        
#     )
#     ) -> None:
#     reqpy.generate_fakeDB()


# # @app.command(
# #         short_help="Provide an analysis on the console of the reqpy database",
# #         )
# # def validate():
# #     res = reqpy.validate_reqpy_database(
# #         mainPath=Path(),
# #         show_console=True
# #     )
# #     raise typer.Exit(code=not res)


# # @app.command(
# #         short_help=(
# #             'delete the existing requirement database'
# #             ' and create an empty database'
# #         )
# #     )
# # def reset():
# #     reqpy.reset_reqpy()


# def _version_callback(value: bool) -> None:
#     if value:
#         typer.echo(f"{__app_name__} v{__version__}")
#         raise typer.Exit()


# @app.callback()
# def common(
#     clx: typer.Context,
#     version: bool = typer.Option(
#         None, "--version", '-v',
#         callback=_version_callback,
#         help="Provide version of the package"
#     ),
# ):
#     pass
