import os
import socket
from typing import List, Optional

from dataclasses import dataclass, asdict, field

import psutil
from pydantic import BaseModel


class EthernetDevice(BaseModel):
    name: str = ''
    mac_address: str = ''
    ip_address: str = ''
    is_virtual: bool = False
    speed_mbps: int = 0
    def parse(self, name:str, mac_address:str, ip_address:str, is_virtual:bool, speed_mbps:int):
        if name:
            self.name = name
        if mac_address:
            self.mac_address = mac_address
        if ip_address:
            self.ip_address = ip_address
        if is_virtual:
            self.is_virtual = is_virtual
        if speed_mbps:
            self.speed_mbps = speed_mbps  # 仅物理网卡填充

    def __repr__(self):
        return (
            f"EthernetDevice(name={self.name}, mac_address={self.mac_address}, "
            f"ip_address={self.ip_address}, is_virtual={self.is_virtual}, "
            f"speed_mbps={self.speed_mbps})"
        )

class EthernetInfo(BaseModel):
    devices: List[EthernetDevice] = field(default_factory=list)
    main_physical_device: Optional[EthernetDevice] = None

    def load(self):
        self.devices = self._get_all_devices()
        self.main_physical_device = self._select_main_physical_device()

    def _get_all_devices(self):
        devices = []

        for nic, addrs in psutil.net_if_addrs().items():
            if nic == "lo":
                continue

            nic_path = f"/sys/class/net/{nic}"
            if not os.path.exists(nic_path):
                continue

            try:
                real_path = os.path.realpath(nic_path)
                is_virtual = "/virtual/" in real_path
            except Exception:
                is_virtual = None

            mac = next((addr.address for addr in addrs if addr.family == psutil.AF_LINK), None)
            ip = next((addr.address for addr in addrs if addr.family == socket.AF_INET), None)

            speed_mbps = None
            if is_virtual is False:
                try:
                    with open(f"/sys/class/net/{nic}/speed", "r") as f:
                        speed_mbps = int(f.read().strip())
                        if speed_mbps < 0:
                            speed_mbps = None
                except Exception:
                    speed_mbps = None

            device = EthernetDevice()
            device.parse(name=nic,
                mac_address=mac,
                ip_address=ip,
                is_virtual=is_virtual,
                speed_mbps=speed_mbps,
            )
            devices.append(device)

        return devices

    def _select_main_physical_device(self):
        candidates = [
            dev for dev in self.devices
            if not dev.is_virtual and dev.ip_address and dev.speed_mbps
        ]
        if not candidates:
            return None
        # 按速度倒序选择最快的一个
        return sorted(candidates, key=lambda d: d.speed_mbps, reverse=True)[0]

    def get_devices(self):
        return self.devices

    def get_main_physical_device(self):
        return self.main_physical_device

    def print_summary(self):
        for dev in self.devices:
            print(f"接口: {dev.name}")
            print(f"  MAC地址: {dev.mac_address}")
            print(f"  IP地址: {dev.ip_address}")
            print(f"  类型: {'虚拟网卡' if dev.is_virtual else '物理网卡'}")
            if dev.speed_mbps is not None:
                print(f"  硬件带宽: {dev.speed_mbps} Mb/s")
            print("-" * 40)

        if self.main_physical_device:
            print("\n主要物理网卡:")
            print(f"  接口: {self.main_physical_device.name}")
            print(f"  IP地址: {self.main_physical_device.ip_address}")
            print(f"  带宽: {self.main_physical_device.speed_mbps} Mb/s")
        else:
            print("\n未检测到主要物理网卡。")



if __name__ == "__main__":
    eth_info = EthernetInfo()
    eth_info.print_summary()
