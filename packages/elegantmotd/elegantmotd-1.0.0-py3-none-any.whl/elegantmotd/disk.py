import shutil
from typing import Dict

from rich.console import RenderableType
from rich.progress import Progress, BarColumn, TaskProgressColumn, TextColumn

from . import themes
from .constants import GB, GREEN, YELLOW, ORANGE, RED
from .sysinfo import SysInfo


class Disk(SysInfo):
    def _get_infos(self) -> Dict[RenderableType, RenderableType]:
        disk_icon = themes.get_icon(self.theme, "disk")
        disk_usage = shutil.disk_usage('/')
        total_space = f"{round(disk_usage.total / GB, 2)}GB"
        usage_percent = round((disk_usage.used / disk_usage.total * 100), 1)
        color = (
            GREEN if usage_percent < 25
            else YELLOW if usage_percent < 50
            else ORANGE if usage_percent < 75
            else RED
        )

        progress = Progress(
            BarColumn(complete_style=color, bar_width=10, finished_style=RED),
            TaskProgressColumn(),
            TextColumn(f" of {total_space}")
        )
        progress.add_task("progress", total=100, completed=round(usage_percent))

        infos = {f"{disk_icon}Usage of /": progress}

        return infos
