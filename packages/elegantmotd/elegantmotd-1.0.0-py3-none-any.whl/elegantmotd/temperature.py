from typing import Dict, Union

import psutil
from rich.console import RenderableType
from rich.text import Text

from . import themes
from .constants import GREEN, YELLOW, ORANGE, RED
from .sysinfo import SysInfo


class Temperature(SysInfo):
    CPU_SENSORS = {
        "coretemp": ["Package", "Core"],
        "k10temp": ["Tctl", "Tdie"]
    }

    def _get_infos(self) -> Dict[RenderableType, RenderableType]:
        temp_icon = themes.get_icon(self.theme, "temperature")
        temp_sensor_icon = themes.get_icon(self.theme, "temp_sensor")
        infos = {f"{temp_icon}Temperature": ""}
        temp_info = psutil.sensors_temperatures()

        for sensor, labels in self.CPU_SENSORS.items():
            if sensor in temp_info:
                for shwtemp in temp_info[sensor]:
                    if any(label in shwtemp.label for label in labels):
                        key = f"{temp_icon}Temperature" if shwtemp.label in labels[
                                                                            :1] else f"{temp_sensor_icon}{shwtemp.label}"
                        infos[key] = self.__get_format_temp(shwtemp)
                return infos

        infos[f"{temp_icon}Temperature"] = "Unable to get CPU temperature"
        return infos

    @staticmethod
    def __get_format_temp(shwtemp) -> Union[str, Text]:
        high = shwtemp.high
        current = shwtemp.current
        if not current:
            return "No data"
        if not high:
            return f"{current}°C"
        if current < high - 40:
            return Text(f"{current}°C", style=GREEN)
        if current < high - 20:
            return Text(f"{current}°C", style=YELLOW)
        if current < high:
            return Text(f"{current}°C", style=ORANGE)
        else:
            return Text(f"{current}°C", style=RED)
