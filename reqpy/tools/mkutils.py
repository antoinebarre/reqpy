""" Utils for the Markdown maangement"""

from enum import Enum, StrEnum, auto
import re

# ============================== ENUMARATES ============================== #


class MyEnum(Enum):
    @classmethod
    def _missing_(cls, value):
        raise ValueError(
                '%r is not a valid %s.  Valid types: %s' % (
                    value,
                    cls.__name__,
                    ', '.join([repr(m.value) for m in cls]),
                    ))


class TextAlignment(MyEnum, StrEnum):
    right = auto()
    left = auto()
    center = auto()  # type: ignore
    justify = auto()


class HeaderLevel(MyEnum):
    TITLE = auto()          # H1 - Main title (largest and most important)
    HEADING = auto()        # H2 - Section headings
    SUBHEADING = auto()     # H3 - Subsection headings
    SUBSUBHEADING = auto()  # H4 - Smaller subsection headings
    MINORHEADING = auto()   # H5 - Even smaller headings
    LEASTHEADING = auto()   # H6 - The smallest heading level

# ============================== TEXT STYLE ============================= #


class TextUtils:
    """This class helps to create bold, italics and change color text."""

    @staticmethod
    def bold(text: str) -> str:
        return "**" + text + "**"

    @staticmethod
    def italics(text: str) -> str:
        return "*" + text + "*"

    @staticmethod
    def inline_code(text: str) -> str:
        return "``" + text + "``"

    @staticmethod
    def center_text(text: str) -> str:
        return "<center>" + text + "</center>"

    @staticmethod
    def text_color(
            text: str,
            color: str = "black"
            ) -> str:
        """Change text color.

        color: it is the text color: ``'orange'``, ``'blue'``, ``'red'``...
                      or a **RGB** color such as ``'#ffce00'``.
        """
        return '<font color="' + color + '">' + text + "</font>"

    @staticmethod
    def text_external_link(
            text: str,
            link: str = ""
            ) -> str:
        return "[" + text + "](" + link + ")"

    @staticmethod
    def insert_code(code: str,
                    language: str = ""
                    ) -> str:
        if language == "":
            return "```\n" + code + "\n```"
        else:
            return "```" + language + "\n" + code + "\n```"

    @staticmethod
    def text_style(
            text: str,
            align: str = "",  # center, right, left or justify
            bold: bool = False,
            italic: bool = False,
            text_color: str = "",  # color name or rgb code
            background_color: str = "",  # color name or rgb code
            font_size: int = 0,  # positive integer
         ) -> str:

        # initiate
        opt_str = ""

        # nested function
        def add_balise(
                opt_str: str,
                balise: str,
                status: str) -> str:
            opt_str += f"{balise}:{status};"
            return opt_str

        # alignement
        if align != "":
            opt_str = add_balise(
                opt_str=opt_str,
                balise="text-align",
                status=TextAlignment(align)
            )

        # BOLD
        if bold:
            opt_str = add_balise(
                opt_str=opt_str,
                balise="font-weight",
                status="bold"
            )
        # ITALIC
        if italic:
            opt_str = add_balise(
                opt_str=opt_str,
                balise="font-style",
                status="italic"
            )

        # COLOR
        if text_color != "":
            opt_str = add_balise(
                opt_str=opt_str,
                balise="color",
                status=text_color,
            )

        # BACKGROUND COLOR
        if background_color != "":
            opt_str = add_balise(
                opt_str=opt_str,
                balise="background-color",
                status=background_color
            )

        # manage output
        if opt_str != "":
            return f"<p style='{opt_str}'>{text}</p>"
        else:
            return text

# =========================== LIST MANAGEMENT =========================== #


class MDListHelper:
    def __init__(self):
        self.n_tabs = 0

    def _get_unordered_markdown_list(self, items, marker: str) -> str:
        md_list = ""
        for item in items:
            if isinstance(item, list):
                self.n_tabs += 1
                md_list += self._get_unordered_markdown_list(item, marker)
                self.n_tabs -= 1
            else:
                md_list += self._add_new_item(item, marker)

        return md_list

    def _get_ordered_markdown_list(self, items) -> str:
        md_list = ""
        n_marker = 1
        for item in items:
            if isinstance(item, list):
                self.n_tabs += 1
                md_list += self._get_ordered_markdown_list(items=item)
                self.n_tabs -= 1
            else:
                md_list += self._add_new_item(item, f"{n_marker}.")
                n_marker += 1
        return md_list

    def _add_new_item(self, item: str, marker: str) -> str:
        item_with_hyphen = (
            item
            if self._is_there_marker_in_item(item)
            else self._add_hyphen(item, marker)
        )
        return self._n_spaces(4 * self.n_tabs) + item_with_hyphen + "\n"

    @classmethod
    def _is_there_marker_in_item(cls, item: str) -> bool:
        if (
            item.startswith("-")
            or item.startswith("*")
            or item.startswith("+")
            or re.search(r"^(\d\.)", item)
        ):
            return True
        return False

    @classmethod
    def _add_hyphen(cls, item: str, marker: str) -> str:
        return f"{marker} {item}"

    @classmethod
    def _n_spaces(cls, number_spaces: int = 1) -> str:
        return " " * number_spaces


class MDList(MDListHelper):
    """This class allows to create unordered or ordered MarkDown list."""

    def __init__(self, items, marked_with: str = "-"):
        """

        :param items: Array of items for generating the list.
        :type items: [str]
        :param marked_with: By default has the value
        of ``'-'``, can be ``'+'``,
          ``'*'``. If you want to generate
         an ordered list then set to ``'1'``.
        :type marked_with: str
        """
        super().__init__()
        self.md_list = (
            self._get_ordered_markdown_list(items)
            if marked_with == "1"
            else self._get_unordered_markdown_list(items, marked_with)
        )

    def get_md(self) -> str:
        """Get the list in markdown format.

        :return:
        :rtype: str
        """
        return self.md_list
