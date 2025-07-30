import json
import os
from typing import Dict, List, Optional
import subprocess

from dataclasses import dataclass, field

from pydantic import BaseModel


class RocmDevice(BaseModel):
    device_name: str = ''
    device_id: str = ''
    guid: str = ''
    unique_id: str = ''
    vbios_version: str = ''
    max_graphics_package_power: float = 0.0
    serial_number: str = ''
    pci_bus: str = ''
    card_series: str = ''
    card_vendor: str = ''

    def load_rocm_device_info(self, value:Dict):
        self.device_name = value.get('Device Name','Unknown')
        self.device_id = value.get('Device ID','Unknown')
        self.guid = value.get('GUID','Unknown')
        self.unique_id = value.get('Unique ID','Unknown')
        self.vbios_version = value.get('VBIOS Version','Unknown')
        self.max_graphics_package_power = float(value.get('Max Graphics Package Power (W)',"0.0"))
        self.serial_number = value.get('Serial Number','Unknown')
        self.pci_bus = value.get('PCI Bus','Unknown')
        self.card_series = value.get('Card Series','Unknown')
        self.card_vendor = value.get('Card Vendor','Unknown')

class RocmInfo(BaseModel):
    cards: List[RocmDevice] = field(default_factory=list)
    card_count: int = 0
    driver_version: str = ''

    def load(self):
        try:
            result = subprocess.run(["rocm-smi", "-a", "--json"], capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            for key in data:
                value = data[key]
                if key.startswith("card"):
                    device = RocmDevice()
                    device.load_rocm_device_info(value)
                    self.cards.append(device)
                if key.startswith("system"):
                    self.driver_version = value.get("Driver Version","Unknown")
            self.card_count = len(self.cards)
        except Exception as e:
            print(e)

    def print_summary(self):
        print("==== ROCm GPU Summary ====")
        print(f"Driver Version: {self.driver_version}")
        print(f"Detected GPU Count: {self.card_count}")
        print("--------------------------")
        for idx, card in enumerate(self.cards):
            print(f"GPU {idx}:")
            print(f"  Device Name      : {card.device_name}")
            print(f"  Device ID        : {card.device_id}")
            print(f"  Card Vendor      : {card.card_vendor}")
            print(f"  Card Series      : {card.card_series}")
            print(f"  Serial Number    : {card.serial_number}")
            print(f"  PCI Bus          : {card.pci_bus}")
            print(f"  Max Power (W)    : {card.max_graphics_package_power}")
            print(f"  VBIOS Version    : {card.vbios_version}")
            print(f"  GUID             : {card.guid}")
            print(f"  Unique ID        : {card.unique_id}")
            print("--------------------------")


class GPUInfo(BaseModel):
    vendor: str = "Unknown"
    rocm_info: Optional['RocmInfo'] = None

    def load(self):
        self.vendor = self.check_gpu_vendor()
        if self.vendor.lower() == "amd":
            self.load_amd()

    def load_amd(self):
        self.rocm_info = RocmInfo()
        self.rocm_info.load()

    def check_gpu_vendor(self):
        try:
            drm_cards = [d for d in os.listdir('/sys/class/drm') if d.startswith('card')]
            for card in drm_cards:
                path = f"/sys/class/drm/{card}/device/vendor"
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        vendor_id = f.read().strip()
                        if vendor_id == '0x1002':
                            return "AMD"
                        elif vendor_id == '0x10de':
                            return "NVIDIA"
                        elif vendor_id == '0x8086':
                            return "Intel"
            return "Unknown"
        except Exception as e:
            return f"Error: {e}"

    def print_summary(self):
        print(f"vendor: {self.vendor}")
        if self.rocm_info is not None:
            self.rocm_info.print_summary()


if __name__ == "__main__":
    gpu_info = GPUInfo()
    gpu_info.load()
    gpu_info.print_summary()



