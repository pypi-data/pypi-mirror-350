import psutil
import platform
import cpuinfo

from pydantic import BaseModel


class CPUInfo(BaseModel):
    vendor: str = ''
    physical_cores: int = 0
    processor_cores: int = 0
    arch: str = ''
    model: str = ''
    logical_cores: int = 0

    def load(self):
        cpu_info = cpuinfo.get_cpu_info()
        self.vendor = cpu_info.get('vendor_id_raw','Unknown')
        self.arch = platform.processor()
        self.model = self._get_cpu_model()
        self.physical_cores = psutil.cpu_count(logical=False)
        self.logical_cores = psutil.cpu_count(logical=True)

    def _get_cpu_model(self) -> str:
        try:
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        return line.strip().split(":")[1].strip()
        except Exception:
            pass
        return "Unknown"

    def print_summary(self):
        print("Vendor: {}".format(self.vendor))
        print("Physical Cores: {}".format(self.physical_cores))
        print("Logical Cores: {}".format(self.logical_cores))
        print("Arch: {}".format(self.arch))
        print("Model: {}".format(self.model))