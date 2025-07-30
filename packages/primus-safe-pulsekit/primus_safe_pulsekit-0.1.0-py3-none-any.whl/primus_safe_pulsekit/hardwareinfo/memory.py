import re
from dataclasses import field, dataclass
from typing import Optional, List
import subprocess
import psutil
from pydantic import BaseModel


class MemoryDevice(BaseModel):
    info_block: str = ""
    array_handle: str = field(init=False, default="Unknown")
    error_info_handle: str = field(init=False, default="Unknown")
    total_width: Optional[int] = field(init=False, default=None)
    data_width: Optional[int] = field(init=False, default=None)
    size: Optional[int] = field(init=False, default=None)
    form_factor: str = field(init=False, default="Unknown")
    set: str = field(init=False, default="Unknown")
    locator: str = field(init=False, default="Unknown")
    bank_locator: str = field(init=False, default="Unknown")
    type: str = field(init=False, default="Unknown")
    type_detail: str = field(init=False, default="Unknown")
    speed: Optional[int] = field(init=False, default=None)
    manufacturer: str = field(init=False, default="Unknown")
    serial_number: str = field(init=False, default="Unknown")
    asset_tag: str = field(init=False, default="Unknown")
    part_number: str = field(init=False, default="Unknown")
    rank: Optional[int] = field(init=False, default=None)
    configured_speed: Optional[int] = field(init=False, default=None)
    min_voltage: Optional[float] = field(init=False, default=None)
    max_voltage: Optional[float] = field(init=False, default=None)
    configured_voltage: Optional[float] = field(init=False, default=None)
    memory_tech: str = field(init=False, default="Unknown")
    operating_mode: str = field(init=False, default="Unknown")
    firmware_version: str = field(init=False, default="Unknown")
    module_manufacturer_id: str = field(init=False, default="Unknown")
    module_product_id: str = field(init=False, default="Unknown")
    controller_manufacturer_id: str = field(init=False, default="Unknown")
    controller_product_id: str = field(init=False, default="Unknown")
    non_volatile_size: str = field(init=False, default="Unknown")
    volatile_size: str = field(init=False, default="Unknown")
    cache_size: str = field(init=False, default="Unknown")
    logical_size: str = field(init=False, default="Unknown")
    
    def parse(self, info_block: str):
        attributes = self._parse_info(info_block)

        # Populate fields
        self.array_handle = attributes.get("Array Handle")
        self.error_info_handle = attributes.get("Error Information Handle")
        self.total_width = self._parse_int(attributes.get("Total Width"))
        self.data_width = self._parse_int(attributes.get("Data Width"))
        self.size = self._parse_size(attributes.get("Size"))
        self.form_factor = attributes.get("Form Factor")
        self.set = attributes.get("Set")
        self.locator = attributes.get("Locator")
        self.bank_locator = attributes.get("Bank Locator")
        self.type = attributes.get("Type")
        self.type_detail = attributes.get("Type Detail")
        self.speed = self._parse_int(attributes.get("Speed"))
        self.manufacturer = attributes.get("Manufacturer")
        self.serial_number = attributes.get("Serial Number")
        self.asset_tag = attributes.get("Asset Tag")
        self.part_number = attributes.get("Part Number")
        self.rank = self._parse_int(attributes.get("Rank"))
        self.configured_speed = self._parse_int(attributes.get("Configured Memory Speed"))
        self.min_voltage = self._parse_float(attributes.get("Minimum Voltage"))
        self.max_voltage = self._parse_float(attributes.get("Maximum Voltage"))
        self.configured_voltage = self._parse_float(attributes.get("Configured Voltage"))
        self.memory_tech = attributes.get("Memory Technology")
        self.operating_mode = attributes.get("Memory Operating Mode Capability")
        self.firmware_version = attributes.get("Firmware Version")
        self.module_manufacturer_id = attributes.get("Module Manufacturer ID")
        self.module_product_id = attributes.get("Module Product ID")
        self.controller_manufacturer_id = attributes.get("Memory Subsystem Controller Manufacturer ID")
        self.controller_product_id = attributes.get("Memory Subsystem Controller Product ID")
        self.non_volatile_size = attributes.get("Non-Volatile Size")
        self.volatile_size = attributes.get("Volatile Size")
        self.cache_size = attributes.get("Cache Size")
        self.logical_size = attributes.get("Logical Size")
        return self

    def _parse_info(self, block: str) -> dict:
        info = {}
        for line in block.splitlines():
            line = line.strip()
            if not line or ":" not in line:
                continue
            key, value = map(str.strip, line.split(":", 1))
            info[key] = value
        return info

    def _parse_int(self, value: Optional[str]) -> Optional[int]:
        if value is None:
            return None
        match = re.search(r"\d+", value)
        return int(match.group()) if match else None

    def _parse_float(self, value: Optional[str]) -> Optional[float]:
        if value is None:
            return None
        match = re.search(r"[\d.]+", value)
        return float(match.group()) if match else None

    def _parse_size(self, value: Optional[str]) -> Optional[int]:
        """Parses memory size like '64 GB' into integer GB."""
        if value is None:
            return None
        match = re.search(r"(\d+)\s*GB", value, re.IGNORECASE)
        return int(match.group(1)) if match else None

    def __repr__(self):
        return f"<MemoryDevice {self.size}GB {self.type} {self.speed}MT/s @ {self.locator}>"

class MemoryInfo(BaseModel):
    total_memory: int = 0
    device_count: int = 0
    devices: List[MemoryDevice] = field(default_factory=list)
    

    def load(self):
        self.total_memory = self._load_memory_total()
        self._load_memory_devices()
        self.device_count = len(self.devices)


    def _load_memory_total(self)->int:
        mem = psutil.virtual_memory()
        return mem.total

    def get_memory_device_blocks(self,dmidecode_output: str) -> List[str]:
        pattern = re.compile(r"Handle .*?\nMemory Device\n(.*?)(?=Handle |\Z)", re.DOTALL)
        return pattern.findall(dmidecode_output)

    def _load_memory_devices(self):
        try:
            process = subprocess.run(args=["sudo","dmidecode", "--type", "memory"]
                                     ,capture_output=True
                                     ,text=True
                                     ,check=True)
            blocks = self.get_memory_device_blocks(process.stdout)
            self.devices = [MemoryDevice().parse(block) for block in blocks if "Size: No Module Installed" not in block]
        except Exception as e:
            print(e)

    def print_summary(self):
        print(f"{self.total_memory}")



if __name__ == "__main__":
    m = MemoryInfo()
    m.load()
    print(m)