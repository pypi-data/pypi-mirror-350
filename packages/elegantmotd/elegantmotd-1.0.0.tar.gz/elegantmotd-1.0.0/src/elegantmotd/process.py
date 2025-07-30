import os
from typing import Dict

from rich.console import RenderableType

from . import themes
from .sysinfo import SysInfo


class Process(SysInfo):
    def _get_infos(self) -> Dict[RenderableType, RenderableType]:
        process_icon = themes.get_icon(self.theme, "processes")
        infos = {f"{process_icon}Processes": str(len(os.listdir("/proc")))}
        return infos
