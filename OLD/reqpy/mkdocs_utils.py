""" MKDOCS UTILS TO HANDLE API"""

from __future__ import annotations
import os
from pathlib import Path
from typing import NamedTuple

import yaml


# ======================= I/O FORMAT DEFINITION ====================== #

class MkdocsConfig(NamedTuple):
    site_name: str
    site_description: str
    plugins: list[str]


DEFAULT_SITE_DESCRIPTION = "System Requirement Specifications"
DEFAULT_PLUGINS = ["with-pdf"]

# TODO : update with
# https://github.com/orzih/mkdocs-with-pdf/blob/master/samples/mkdocs-material/mkdocs.yml


class MkdocsProjectPath(NamedTuple):
    docsPath: Path
    indexPath: Path
    configPath: Path

    @classmethod
    def fromProjectPath(
            cls,
            projectPath: Path
        ) -> MkdocsProjectPath:

        return cls(
            docsPath=projectPath / "docs",
            indexPath=projectPath / "docs" / "index.md",
            configPath=projectPath / "mkdocs.yml"
        )

def newMKdocs(
        projectPath: Path
        ) -> MkdocsProjectPath:

    os.system(
        f'mkdocs -v new {str(projectPath.absolute())}')

    return MkdocsProjectPath.fromProjectPath(projectPath)

def buildMKdocs(
        configfilePath: Path,
        sitePath: Path
                ):
    os.system(("mkdocs build " +
               f"--config-file {str(configfilePath.absolute())} " +
               f"--site-dir {str(sitePath.absolute())}"))


def set_MKDOCS_configuration(
        configFilePath: Path,
        title: str
        ):

    configData = MkdocsConfig(
        site_name=title,
        site_description=DEFAULT_SITE_DESCRIPTION,
        plugins=DEFAULT_PLUGINS
    )
    data = configData._asdict()

    with open(configFilePath, 'w+') as file:
        yaml.safe_dump(
            data,
            file,
            sort_keys=False)


def createMkDocsServer(
        configfilePath: Path,
        ):
    os.system(("mkdocs serve " +
               f"--config-file {str(configfilePath.absolute())} " +
               "--theme material"
               ))
