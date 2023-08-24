""" Markdown support tools"""


from .mkutils import HeaderLevel, MDList, TextUtils

__all__ = [
    "MDText",
]


class MDText():
    """_summary_

    Returns
    -------
    _type_
        _description_
    """

# =============================CONSTRUCTOR============================= #

    def __init__(self):
        self.textUtils = TextUtils
        self._mdContent = ""

    def __str__(self) -> str:
        return self._mdContent

    def ___update_mdContent(self, data):
        self._mdContent += data

# =============================== HEADERS =============================== #

    def add_header(
            self,
            *,
            level: int,
            title: str,
            ) -> None:

        if title != "":
            self.___update_mdContent(
                data=(
                    "\n" +
                    "#" * HeaderLevel(level).value +
                    " " +
                    title.capitalize() +
                    "\n")
            )

    def add_title(
            self,
            title: str,
    ) -> None:
        self.add_header(level=1, title=title.upper())

# ============================== PARAGRAPH ============================= #

    def add_paragraph(
            self,
            *,
            text: str,
            ) -> None:
        if text != "":
            self.___update_mdContent(
                data=(
                     "\n\n" +
                     text +
                     "\n"
                     )
            )

# =============================== NEWLINE ============================== #
    def add_newline(
            self,
            ) -> None:
        self.___update_mdContent(
            data="  \n"
        )

# ================================= LIST ================================ #
    def add_list(
            self,
            items: list,
            marker: str = "1"
            ) -> None:
        mdList = MDList(items, marked_with=marker)

        self.___update_mdContent(
            "\n" +
            mdList.get_md()
        )
