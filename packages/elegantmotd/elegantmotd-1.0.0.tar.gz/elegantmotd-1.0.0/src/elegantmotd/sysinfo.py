from abc import ABC, abstractmethod
from typing import Dict

from rich.console import RenderableType


class SysInfo(ABC):
    def __init__(self, theme: str):
        self.theme = theme
        self.infos = self._get_infos()

    @abstractmethod
    def _get_infos(self) -> Dict[RenderableType, RenderableType]:
        pass
