#!/usr/bin/python


import os
import sys
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

@cli.command(name="fakeDB")
@click.option(
    '-d', '--dir',
    default=Path(),
    type=click.Path(),
    help=(
        "The directory to create the fake database."
        " [default: current directory]"
        ))
def create_fakeDB(dir,):
    """Create a fake Reqpy Database for test or support"""
    reqpy.generate_fakeDB(path=Path(dir))




if __name__ == '__main__':  # pragma: no cover
    cli()
