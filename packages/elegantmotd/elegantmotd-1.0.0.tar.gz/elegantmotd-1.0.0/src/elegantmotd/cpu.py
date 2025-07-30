from typing import Dict

import psutil
from rich.console import RenderableType
from rich.progress import Progress, BarColumn, TaskProgressColumn

from . import themes
from .constants import GREEN, RED, ORANGE, YELLOW
from .sysinfo import SysInfo


class CPU(SysInfo):
    def _get_infos(self) -> Dict[RenderableType, RenderableType]:
        cpu_icon = themes.get_icon(self.theme, "cpu")
        cpu_percent = psutil.cpu_percent()
        color = (
            GREEN if cpu_percent < 25
            else YELLOW if cpu_percent < 50
            else ORANGE if cpu_percent < 75
            else RED
        )
        progress = Progress(
            BarColumn(complete_style=color, bar_width=10, finished_style=RED),
            TaskProgressColumn()
        )
        progress.add_task("cpu_percent", total=100, completed=round(cpu_percent))
        infos = {f"{cpu_icon}CPU": progress}
        return infos
