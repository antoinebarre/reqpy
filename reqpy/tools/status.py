
from __future__ import annotations
from typing import Iterable
from prettytable import PrettyTable
from pydantic import BaseModel, ConfigDict, field_validator


class CheckStatus(BaseModel):
    """
    A class representing a status check result.

    Attributes:
        valid (bool): Indicates whether the check status is valid or not.
        message (list[str]): List of messages associated with the check status.
    """
    # -------------------------- CONFIGURATION ------------------------- #
    check: str  # description of the check
    valid: bool  # valid against the check
    message: str  # message if invalid else ""

    # -------------------------- CONFIGURATION ------------------------- #
    model_config = ConfigDict(
        extra='forbid',
        validate_assignment=True,
        frozen=True,
        )

    # ---------------------------- VALIDATOR --------------------------- #
    @field_validator("check")
    def validate_ids_length(cls, value):
        if len(value) == 0:
            raise ValueError("Empty string for check Name is not permitted")
        return value
    # --------------------------- CONSTRUCTOR -------------------------- #

    def __init__(
            self,
            check: str,
            valid: bool,
            message: str,
            **kwargs
            ):

        if valid is True and message != "":
            raise ValueError(
                ("For Checkstatus object message is not"
                 " permitted if the check is valid"))
        elif valid is False and message == "":
            raise ValueError(
                ("Empty rationale for a failled check is not permitted"))
        else:
            super().__init__(
                check=check,
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
                f"Check   : {self.check}\n" +
                f"Valid   : {self.valid}\n" +
                f"Messages: {self.message}")
        else:
            msg = (
                f"Check   : {self.check}\n" +
                f"Valid: {self.valid}\n"
            )
        return msg

    # --------------------------- PROPERTIES --------------------------- #

    # ----------------------------- METHODS ---------------------------- #
    @staticmethod
    def createValid(checkName) -> CheckStatus:
        return CheckStatus(
            check=checkName,
            valid=True,
            message=""
        )


class CheckStatusList(list):
    # --------------------------- CONSTRUCTOR -------------------------- #
    def __init__(self, iterable: Iterable[CheckStatus]):
        if all(isinstance(item, CheckStatus) for item in iterable):
            super().__init__(
                item for item in iterable
                )
        else:
            raise TypeError(
                "all elements of the iterable shall be a CheckStatus object")
    # --------------------------- PROPERTIES --------------------------- #

    # ----------------------------- METHODS ---------------------------- #

    def append(self, item):
        if isinstance(item, CheckStatus):
            super().append(str(item))
        else:
            raise TypeError(
                "Inapropriate type to append to a Checkstatus List."
                " It shall be a Checkstatus"
            )

    def extend(self, other):
        if isinstance(other, type(self)):
            super().extend(other)
        else:
            raise TypeError(
                "Inapropriate type to append to a Checkstatus List."
                " It shall be a Checkstatus"
            )

    def is_valid(self) -> bool:
        return all(
            [elt.valid for elt in self]
        )

    def tostr(self: CheckStatusList) -> str:

        # creating an empty PrettyTable
        x = PrettyTable()

        x.field_names = [
            "Check",
            "Is Valid",
            "Rationale",
        ]

        # column width
        x._max_width = {
            "Check": 30,
            "Rationale": 30,
            }
        #
        x.align["Check"] = "l"
        x.align["Rationale"] = "l"

        for elt in self:
            x.add_row([
                elt.check,
                elt.valid,
                elt.message
                ])
        return str(x)
