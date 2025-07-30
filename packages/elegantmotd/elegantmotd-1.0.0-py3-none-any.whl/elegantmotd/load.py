import os
from typing import Dict

from rich.console import RenderableType

from . import themes
from .sysinfo import SysInfo


class Load(SysInfo):
    def _get_infos(self) -> Dict[RenderableType, RenderableType]:
        load_icon = themes.get_icon(self.theme, "load")
        infos = {
            f"{load_icon}System load": str(os.getloadavg()[0])
        }
        return infos
