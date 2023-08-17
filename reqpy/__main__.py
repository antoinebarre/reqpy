#!/usr/bin/python


import os
import sys
from __init__ import __version__
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
    message=(
        '%(prog)s, version %(version)s from'
        f' { PKG_DIR } (Python { PYTHON_VERSION })'
         ),
)
def cli():
    """
    reqpy - Requirements Management Tools based on YAML
    """


# ============================= CREATE DEMO ============================= #

@cli.command(name="createDemo")
@click.option(
    '-d', '--dir',
    default=Path(),
    type=click.Path(),
    help=(
        "The directory to create the demo database."
        " [default: current directory]"
        ))
def create_fakeDB(dir,):
    """Create a fake Reqpy Database for test or support"""
    raise click.ClickException("createdemo features is not implemented")


if __name__ == '__main__':  # pragma: no cover
    cli()
