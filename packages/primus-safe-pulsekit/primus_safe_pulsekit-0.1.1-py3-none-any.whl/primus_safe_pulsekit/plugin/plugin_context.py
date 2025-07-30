from typing import Dict, Optional
from primus_safe_pulsekit.hardwareinfo.hardware_info import HardwareInfo

class PluginContext:
    def __init__(
        self,
        hardware_info: HardwareInfo,
        env: Optional[Dict[str, str]] = None,
        extra: Optional[Dict[str, str]] = None,
        args: Optional[Dict[str,str]] = None
    ):
        self.env = env or {}
        self.hardware_info = hardware_info
        self.extra = extra or {}
        self.args = args or {}

    def get_env(self, key: str, default=None):
        return self.env.get(key, default)

    def set_env(self, key: str, value: str):
        self.env[key] = value
