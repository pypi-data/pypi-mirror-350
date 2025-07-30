import subprocess
from typing import Dict

from rich.console import RenderableType

from . import themes
from .sysinfo import SysInfo


class LoggedInUsers(SysInfo):
    def _get_infos(self) -> Dict[RenderableType, RenderableType]:
        nb = len(subprocess.run(["who"], capture_output=True).stdout.split(b"\n")) - 1
        user_icon = themes.get_icon(self.theme, "users")
        infos = {f"{user_icon}Users logged in": str(nb)}
        return infos
