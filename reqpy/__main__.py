# #!/usr/bin/python
from __future__ import annotations
from reqpy.tools.paths import test_toto


print("hello")
test_toto()
# import os
# import sys
# from reqpy.tools.paths import test_toto

# from pathlib import Path
# import click

# __version__ = "0.0.1"
# PYTHON_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}"
# PKG_DIR = os.path.dirname(os.path.abspath(__file__))


# @click.group(
#         context_settings=dict(help_option_names=['-h', '--help'],
#                               max_content_width=120))
# @click.version_option(
#     __version__,
#     '-V',
#     '--version',
#     message=(
#         '%(prog)s, version %(version)s from'
#         f' { PKG_DIR } (Python { PYTHON_VERSION })'
#          ),
# )
# def cli():
#     """
#     reqpy - Requirements Management Tools based on YAML
#     """


# # ============================= CREATE DEMO ============================= #

# @cli.command(name="createDemo")
# @click.option(
#     '-d', '--dir',
#     default=Path(),
#     type=click.Path(),
#     help=(
#         "The directory to create the demo database."
#         " [default: current directory]"
#         ))
# def create_fakeDB(dir,):
#     """Create a fake Reqpy Database for test or support"""
#     raise click.ClickException("createdemo features is not implemented")


# if __name__ == '__main__':  # pragma: no cover
#     cli()
