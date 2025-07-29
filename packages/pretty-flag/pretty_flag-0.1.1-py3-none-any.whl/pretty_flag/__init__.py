from rich.panel import Panel
from rich.align import Align
from rich.padding import Padding
from rich.console import Group
from rich.text import Text
from rich import box
from rich import print as rprint

def print_flag(flag: str, host: str | None = None,user: str | None = None, password: str | None = None) -> None:
    header = Text.from_markup("[blink bold cyan]  FLAG  [/]")
    body = Text.from_markup(f"[blink bold light_green]  {flag}  [/]")
    content = Group(
        Align.center(header),
        Padding(Align.center(body), (1, 0, 0, 0)),
    )
    panel = Panel(
        content,
        box=box.DOUBLE,
        border_style="bright_blue",
        title=None if host is None else f"[bold magenta]{host}[/]",
        title_align="right",
        subtitle=None if user is None or password is None else f"[green]{user}@{password}[/]",
        subtitle_align="left",
        padding=(1, 4),
        expand=False,
    )
    rprint(Align.center(panel))