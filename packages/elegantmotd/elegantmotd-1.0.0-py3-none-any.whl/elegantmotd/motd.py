import getpass
import platform
import sys
import time
from datetime import datetime, timezone

import distro
import rich_click as click
from art import text2art
from rich.console import Console
from rich.live import Live
from rich.padding import Padding
from rich.style import Style
from rich.table import Table

from . import themes
from .cpu import CPU
from .disk import Disk
from .load import Load
from .loggedinusers import LoggedInUsers
from .memory import Memory
from .network import Network
from .process import Process
from .temperature import Temperature


def get_distro_info():
    return f"{distro.id().capitalize()} {distro.version()} {distro.codename()}"


def get_kernel_info():
    return platform.release()


def get_architecture():
    return platform.machine()


@click.command(help="Display system information in a visually appealing manner")
@click.option("-w", "--watch", is_flag=True, show_default=False, default=False,
              help="Enable live updates of the system information")
@click.option("-t", "--theme", type=click.Choice(["none", "emoji", "nerdfont"]), default="none",
              help="Choose a visual theme")
def display(watch: bool, theme: str) -> None:
    console = Console()
    try:
        distro_info = get_distro_info()
        kernel = get_kernel_info()
        architecture = get_architecture()

        if watch:
            console.clear()

        art_user = "\n".join(
            " " + line for line in text2art(getpass.getuser(), font='small').split("\n")[:-1])

        os_icon = themes.get_icon(theme, "os")
        console.print(
            f"{os_icon}[blue bold]{distro_info} LTS (GNU/Linux {kernel} {architecture}) [/]{os_icon}")
        console.print(f"[orange1 bold]{art_user}[/]")
        padding = Padding(generate_table(theme), (0, 0, 1, 0))
        if watch:
            with Live(padding, refresh_per_second=1) as live:
                while True:
                    time.sleep(1)
                    padding.renderable = generate_table(theme)
                    live.update(padding)
        else:
            console.print(padding)
    except KeyboardInterrupt:
        console.clear()


def generate_table(theme: str) -> Table:
    local_time = datetime.now(timezone.utc).astimezone()
    utc_offset = round(local_time.utcoffset().total_seconds() / 3600)
    title_icon = themes.get_icon(theme, "title")
    clock_icon = themes.get_icon(theme, "time")
    calendar_icon = themes.get_icon(theme, "date")
    table = Table(
        show_header=False,
        box=None,
        title_justify="left",
        title=(
            f" {title_icon}System information as of {local_time.strftime(f'{calendar_icon}%a. %d %B %Y {clock_icon}%H:%M:%S')} "
            f"UTC+{utc_offset}\n"
        ),
        title_style=Style(color="white", italic=False, bold=True),
        expand=True,
        leading=1,
        padding=(0, 2)
    )
    table.add_column("Info", style="bold CYAN")
    table.add_column("Value", style="bold WHITE")
    sysinfos = [
        Load(theme),
        Disk(theme),
        Memory(theme),
        Temperature(theme),
        Process(theme),
        LoggedInUsers(theme),
        Network(theme),
        CPU(theme)
    ]
    [table.add_row(f"{info}:", sysinfo.infos[info])
     for sysinfo in sysinfos for info in sysinfo.infos]
    return table


if __name__ == '__main__':
    display(sys.argv[1:])
