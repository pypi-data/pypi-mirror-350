from pydantic import BaseModel

from .cpu import CPUInfo
from .gpu import GPUInfo
from .ethernet import EthernetInfo
from .memory import MemoryInfo
from dataclasses import dataclass, field, asdict


class HardwareInfo(BaseModel):
    cpu: CPUInfo = field(default_factory=lambda: CPUInfo())
    gpu: GPUInfo = field(default_factory=lambda: GPUInfo())
    memory: MemoryInfo = field(default_factory=lambda: MemoryInfo())
    ethernet: EthernetInfo = field(default_factory=lambda: EthernetInfo())

    def load(self):
        for name, component in self.__dict__.items():
            if component is not None and hasattr(component, 'load') and callable(getattr(component, 'load')):
                try:
                    component.load()
                except Exception as e:
                    print(f"Failed to load {name}: {e}")

    def print_summary(self):
        for name, component in self.__dict__.items():
            if component is not None and hasattr(component, 'print_summary') and callable(getattr(component, 'load')):
                try:
                    print(f"{name}:")
                    component.print_summary()
                except Exception as e:
                    print(f"Failed to print_summary {name}: {e}")




def get_hardware_info() -> HardwareInfo:
    hw_info = HardwareInfo()

    hw_info.load()
    return hw_info
