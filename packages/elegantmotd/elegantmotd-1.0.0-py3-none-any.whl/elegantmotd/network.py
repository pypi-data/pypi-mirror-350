from socket import AF_INET
from typing import Dict

import psutil
from rich.console import RenderableType

from . import themes
from .sysinfo import SysInfo


class Network(SysInfo):
    def _get_infos(self) -> Dict[RenderableType, RenderableType]:
        network_icon = themes.get_icon(self.theme, "network")
        net_iface_icon = themes.get_icon(self.theme, "net_iface")
        infos = {f"{network_icon}Network": ""}

        addrs = psutil.net_if_addrs()
        for intf, addr_list in addrs.items():
            if intf != "lo":
                for addr in addr_list:
                    if addr.family == AF_INET:
                        infos[f"{net_iface_icon}{intf}"] = addr.address

        return infos
