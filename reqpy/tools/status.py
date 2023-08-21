
from __future__ import annotations
from pydantic import BaseModel, ConfigDict


class CheckStatus(BaseModel):
    """
    A class representing a status check result.

    Attributes:
        valid (bool): Indicates whether the check status is valid or not.
        message (list[str]): List of messages associated with the check status.
    """
    # -------------------------- CONFIGURATION ------------------------- #
    valid: bool
    message: list[str]

    # -------------------------- CONFIGURATION ------------------------- #
    model_config = ConfigDict(
        extra='forbid',
        validate_assignment=True,
        frozen=True,
        )

    # ---------------------------- VALIDATOR --------------------------- #

    # --------------------------- CONSTRUCTOR -------------------------- #

    def __init__(
            self,
            valid: bool,
            message: list[str],
            **kwargs
            ):
        """
        Constructs a CheckStatus instance.

        Args:
            valid (bool): Indicates whether the check status is valid or not.
            message (list[str]): List of messages associated with the check status.
            **kwargs: Additional keyword arguments.
        """
        if valid is True:
            message = []

        super().__init__(
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

        nb_issues = len(self.message)
        if nb_issues > 0:
            msg = (
                f"Valid: {self.valid}\n" +
                f"Messages: (nb of issues: {nb_issues})\n" +
                "\n".join(self.message)
            )
        else:
            msg = (
                f"Valid: {self.valid}\n"
            )
        return msg

    def __add__(
            self,
            otherSelf: CheckStatus
            ) -> CheckStatus:
        """
        Adds the statuses of two CheckStatus instances.

        Args:
            otherSelf (CheckStatus): Another CheckStatus instance to add.

        Returns:
            CheckStatus: New CheckStatus instance with combined statuses.
        """
        newValid = self.valid and otherSelf.valid
        newMessage = self.message + otherSelf.message
        return CheckStatus(
            valid=newValid,
            message=newMessage,
        )

    # --------------------------- PROPERTIES --------------------------- #

    @property
    def nb_status(self) -> int:
        """
        Returns the number of status messages.

        Returns:
            int: Number of status messages.
        """
        return len(self.message)

    # ----------------------------- METHODS ---------------------------- #
