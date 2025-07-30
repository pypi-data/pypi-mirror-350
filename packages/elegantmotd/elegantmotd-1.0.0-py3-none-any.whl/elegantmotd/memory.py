from typing import Dict

import psutil
from rich.console import RenderableType
from rich.progress import Progress, BarColumn, TaskProgressColumn, TextColumn

from . import themes
from .constants import GB, GREEN, YELLOW, ORANGE, RED
from .sysinfo import SysInfo


class Memory(SysInfo):
    def _get_infos(self) -> Dict[RenderableType, RenderableType]:
        memory_icon = themes.get_icon(self.theme, "memory")
        memory_usage = psutil.virtual_memory()
        memory_progress, memory_usage_percent = self.__get_process(memory_usage)
        memory_progress.add_task("memory_progress", total=100, completed=round(memory_usage_percent))

        swap_icon = themes.get_icon(self.theme, "swap")
        swap_usage = psutil.swap_memory()
        swap_progress, swap_usage_percent = self.__get_process(swap_usage)
        swap_progress.add_task("swap_progress", total=100, completed=round(swap_usage_percent))

        infos = {f"{memory_icon}Memory usage": memory_progress, f"{swap_icon}Swap usage": swap_progress}
        return infos

    @staticmethod
    def __get_process(usage):
        total_space = f"{round(usage[0] / GB, 2)}GB"
        usage_percent = usage[2]
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
        return progress, usage_percent
