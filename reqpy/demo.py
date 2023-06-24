""" Package with all function used to generate a demo requirement database
"""

import pathlib

from reqpy.requirements import Requirement
from reqpy.database import ReqFolder
from reqpy.__settings import FolderStructure
from reqpy.utils import generate_random_string, randomText

from faker import Faker


def generate_DB(
        nbFilesPerFolder: int = 10,  # number of files per folder
        nbFolder: int = 5,  # number of additional folder in requirement
        path: pathlib.Path = pathlib.Path()  # path where the DB is created
) -> None:

    # create a ReqFolder object
    reqF = ReqFolder(rootdir=path)

    # reset the existing folder
    reqF.clean_dirs()
    reqF.create_dirs()

    # create a fake instance
    fake = Faker()

    # get the requirement rootdir
    req_rootDir = path / FolderStructure.main_folder

    # create the list of folder
    list_folders = [
        req_rootDir / generate_random_string(30)
        for _ in range(nbFolder)
        ]
    list_folders.append(req_rootDir)

    for folder in list_folders:
        # create folder
        folder.mkdir(exist_ok=True)

        for _ in range(nbFilesPerFolder):
            req = Requirement(
                title=generate_random_string(40).capitalize(),
                detail=fake.text(max_nb_chars=2000),
                rationale=randomText(),
                )
            req.write(
                folderPath=folder
            )
