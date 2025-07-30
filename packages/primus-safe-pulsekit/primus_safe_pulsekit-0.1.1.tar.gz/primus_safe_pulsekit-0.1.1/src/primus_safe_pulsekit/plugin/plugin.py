from enum import Enum
from abc import ABC, abstractmethod
from typing import Dict, Any
from primus_safe_pulsekit.util import ProgressReporter
from primus_safe_pulsekit.dsl.dsl import evaluate_dsl
from primus_safe_pulsekit.plugin import PluginContext

class PluginType(Enum):
    Builtin = "builtin"
    Remote = "remote"

class PluginBase(ABC):
    name: str = "BasePlugin"
    dsl_requirement: Dict[str, Any] = {}

    def check_enabled(self, context: PluginContext) -> bool:
        if context.hardware_info is None:
            return True  # or False, based on your policy
        return evaluate_dsl(self.dsl_requirement, context.hardware_info)

    @abstractmethod
    def install_dependencies(self, context: PluginContext, progress: ProgressReporter):
        ...

    @abstractmethod
    def run(self, context: PluginContext, progress: ProgressReporter) -> str:
        ...

    @abstractmethod
    def get_json_result(self, output: str) -> Dict[str, Any]:
        ...

    @abstractmethod
    def get_type(self)->PluginType:
        ...
