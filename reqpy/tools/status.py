
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from prettytable import PrettyTable
from pydantic import BaseModel, ConfigDict, field_validator


class CheckStatus(BaseModel):
    """
    A class representing a status check result.

    This class encapsulates the result of a status check operation, providing
    information about the validity of the check and associated messages.

    Attributes:
        check (str): A description of the performed check.
        valid (bool): Indicates whether the check status is valid or not.
        message (str): An optional message associated with the check status,
         providing additional context when the check is invalid.
    """
    # -------------------------- CONFIGURATION ------------------------- #
    checkName: str  # description of the check
    valid: bool  # valid against the check
    message: str  # message if invalid else ""

    # -------------------------- CONFIGURATION ------------------------- #
    model_config = ConfigDict(
        extra='forbid',
        validate_assignment=True,
        frozen=False,
        )

    # ---------------------------- VALIDATOR --------------------------- #
    @field_validator("checkName")
    def validate_ids_length(cls, value):
        if len(value) == 0:
            raise ValueError("Empty string for check Name is not permitted")
        return value
    # --------------------------- CONSTRUCTOR -------------------------- #

    def __init__(
            self,
            checkName: str,
            valid: bool,
            message: str,
            **kwargs
            ):
        """
        Initialize a CheckStatus instance.

        Args:
            checkName (str): Description of the check.
            valid (bool): Valid against the check.
            message (str): Message if invalid, else "".
            **kwargs: Additional keyword arguments.
        """

        if valid is True and message != "":
            raise ValueError(
                ("For Checkstatus object message is not"
                 " permitted if the check is valid"))
        elif valid is False and message == "":
            raise ValueError(
                ("Empty rationale for a failled check is not permitted"))
        else:
            super().__init__(
                checkName=checkName,
                valid=valid,
                message=message,
                **kwargs
                )

    # ------------------------- DUNDER METHODS ------------------------- #
    def __str__(self):
        """
        Returns a string representation of the check status.

        Returns:
            str: String representation of the check status.
        """

        if self.valid is False:
            msg = (
                f"Check   : {self.checkName}\n" +
                f"Valid   : {self.valid}\n" +
                f"Messages: {self.message}")
        else:
            msg = (
                f"Check   : {self.checkName}\n" +
                f"Valid: {self.valid}\n"
            )
        return msg

    # --------------------------- PROPERTIES --------------------------- #

    # ----------------------------- METHODS ---------------------------- #
    @staticmethod
    def createValid(checkName: str) -> CheckStatus:
        """
        Create a CheckStatus instance that represents a valid check.

        Args:
            checkName (str): The name of the check.

        Returns:
            CheckStatus: A CheckStatus instance representing a valid check.
        """
        return CheckStatus(
            checkName=checkName,
            valid=True,
            message=""
        )


class CheckStatusList(list):
    """
    A list subclass for managing CheckStatus instances.

    This class extends the built-in list class to manage a list of CheckStatus
    instances.

    Attributes:
        None
    """
    # --------------------------- CONSTRUCTOR -------------------------- #
    def __init__(self, iterable: Iterable[CheckStatus]):
        """
        Initialize a CheckStatusList instance.

        Args:
            iterable (Iterable[CheckStatus]): An iterable of CheckStatus
            instances.
        """
        if all(isinstance(item, CheckStatus) for item in iterable):
            super().__init__(
                item for item in iterable
                )
        else:
            raise TypeError(
                "all elements of the iterable shall be a CheckStatus object")
    # --------------------------- PROPERTIES --------------------------- #

    # ----------------------------- METHODS ---------------------------- #

    def append(self, item: CheckStatus):
        """
        Append a CheckStatus instance to the list.

        Args:
            item (CheckStatus): The CheckStatus instance to append.
        """
        if isinstance(item, CheckStatus):
            super().append(item)
        else:
            raise TypeError(
                "Inapropriate type to append to a Checkstatus List."
                " It shall be a Checkstatus"
            )

    def extend(self, other):
        """
        Extend the list with the elements from another CheckStatusList.

        Args:
            other (CheckStatusList): Another CheckStatusList to extend with.
        """
        if isinstance(other, type(self)):
            super().extend(other)
        else:
            raise TypeError(
                "Inapropriate type to append to a Checkstatus List."
                " It shall be a Checkstatus"
            )

    def is_valid(self) -> bool:
        """
        Check if all CheckStatus instances in the list are valid.

        Returns:
            bool: True if all instances are valid, False otherwise.
        """
        return all(
            [elt.valid for elt in self]
        )
    
    def getErrorsMessages(self: CheckStatusList) -> list[str]:
        return [
            elt.message for elt in self.extract_error()
        ]

    def tostr(self: CheckStatusList) -> str:
        """
        Generate a formatted string representation of the CheckStatusList.

        Returns:
            str: A formatted string representation of the CheckStatusList.
        """

        # creating an empty PrettyTable
        x = PrettyTable()

        x.field_names = [
            "Check",
            "Is Valid",
            "Rationale",
        ]

        # column width
        x._max_width = {
            "Check": 50,
            "Rationale": 50,
            }
        #
        x.align["Check"] = "l"
        x.align["Rationale"] = "l"

        for elt in self:
            x.add_row([
                elt.checkName,
                elt.valid,
                elt.message
                ])
        return str(x)

    def extract_error(self: list[CheckStatus]):
        return CheckStatusList(
            [elt for elt in self if not elt.valid])


@dataclass
class FileStatus():
    # ------------------------------ MODEL ----------------------------- #
    filePath: Path
    checks: CheckStatusList

    # --------------------------- VALIDATION --------------------------- #
    def __post_init__(self):
        if not isinstance(self.filePath, Path):
            raise TypeError('filePath shall be of type pathlib.Path')

        if not isinstance(self.checks, CheckStatusList):
            raise TypeError('checks shall be of type CheckStatusList')

    # --------------------------- CONSTRUCTOR -------------------------- #

    # ----------------------------- METHODS ---------------------------- #

    def addCheckResult(
            self,
            result: CheckStatus
            ) -> None:
        self.checks.append(result)

    def addCheckResultList(
            self,
            resultList: CheckStatusList
            ) -> None:
        self.checks.extend(resultList)

    def isValidFile(self) -> bool:
        return self.checks.is_valid()

    def relative_to(self, baseFolder: Path) -> str:
        return str(self.filePath.relative_to(baseFolder))


class FileStatusList(list):
    def __init__(self, iterable: Iterable[CheckStatus]):
        if all(isinstance(item, FileStatus) for item in iterable):
            super().__init__(
                item for item in iterable
                )
        else:
            raise TypeError(
                "all elements of the iterable shall be a FilsStatus object")

    def append(self, item: FileStatus):
        if isinstance(item, FileStatus):
            super().append(item)
        else:
            raise TypeError(
                "Inapropriate type to append to a FileStatus List."
                " It shall be a FileStatus"
            )

    def isAllFilesValid(self: list[FileStatus]) -> bool:
        return all(
            [elt.isValidFile() for elt in self]
        )

    def printResults(self: list[FileStatus]):
        for res in self:
            print(f"File: {res.filePath} - {res.isValidFile()}")
