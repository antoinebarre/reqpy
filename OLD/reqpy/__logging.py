"""logging tools for reqpy module"""


from typing import Iterable, Sequence, TypeVar, Union
from rich.console import Console
from rich.theme import Theme
from rich.progress import track
from loguru import logger as log


ProgressType = TypeVar("ProgressType")

# Define console Theme
custom_theme = Theme({
    "title": "bold white on dodger_blue3",
    "apps": "bold blue",
    "activity": "purple italic",
    "info": "cyan",
    "ok": "green",
    "ko": "red",
    "warning": "red on yellow",
    "error": "bold yellow on red",
    })

console = Console(theme=custom_theme)


class Myconsole:
    @staticmethod
    def __publishConsole(
            *,
            message: str,
            theme: str,
            before: str = "",
            after: str = "",
            align: str = "left",
            show_console: bool,
            ):
        if show_console:
            message = (before +
                       message +
                       after)
            # print in Console

            console.print(
                message,
                style=theme,
                justify=align)  # type: ignore
            # log
            log.trace(f"Console Ouputs: [{theme}] {message}")

    @staticmethod
    def title(msg: str, show_console: bool = True) -> None:
        Myconsole.__publishConsole(
            message=msg.upper(),
            theme="title",
            align="center",
            show_console=show_console,
        )
        return None

    @staticmethod
    def apps(msg: str, show_console: bool = True) -> None:
        Myconsole.__publishConsole(
            message=msg.upper(),
            theme="apps",
            before=">>> ",
            after="",
            show_console=show_console,
        )

    @staticmethod
    def task(msg: str, show_console: bool = True) -> None:
        Myconsole.__publishConsole(
            message=msg,
            theme="activity",
            before=" - ",
            after="...",
            show_console=show_console,
        )

    @staticmethod
    def info(msg: str, show_console: bool = True) -> None:
        Myconsole.__publishConsole(
            message=msg,
            theme="info",
            show_console=show_console,
        )

    @staticmethod
    def ok(msg: str, show_console: bool = True) -> None:
        Myconsole.__publishConsole(
            message=msg,
            theme="ok",
            show_console=show_console,
        )

    @staticmethod
    def ko(msg: str, show_console: bool = True) -> None:
        Myconsole.__publishConsole(
            message=msg,
            theme="ko",
            show_console=show_console,
        )

    @staticmethod
    def warning(msg: str, show_console: bool = True) -> None:
        Myconsole.__publishConsole(
            message=msg,
            theme="warning",
            before="WARNING: ",
            show_console=show_console,
        )

    @staticmethod
    def error(msg: str, show_console: bool = True) -> None:
        Myconsole.__publishConsole(
            message=msg,
            theme="error",
            before="ERROR: ",
            show_console=show_console,
        )

    @staticmethod
    def progressBar(
         sequence: Union[Sequence[ProgressType], Iterable[ProgressType]],
         description: str = "Working...",
         show_console: bool = True
         ) -> Iterable[ProgressType]:

        return track(
            sequence=sequence,
            description=description,
            disable=not show_console)
