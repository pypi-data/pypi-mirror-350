import json
from typing import Any, Dict
import operator
from primus_safe_pulsekit.hardwareinfo.hardware_info import HardwareInfo


def get_by_path(data: Any, path: str) -> Any:
    parts = path.strip().split('.')
    for part in parts:
        if isinstance(data, list):
            if part == '*':
                return [get_by_path(item, '.'.join(parts[1:])) for item in data]
            else:
                data = data[int(part)]
        elif isinstance(data, dict):
            data = data.get(part)
        else:
            return None
    return data


def evaluate_dsl(dsl: Dict[str, Any], context: HardwareInfo) -> bool:
    OP_MAP = {
        'eq': operator.eq,
        'neq': operator.ne,
        'gt': operator.gt,
        'gte': operator.ge,
        'lt': operator.lt,
        'lte': operator.le,
        'contains': lambda x, y: y in x,
    }

    context_dict = json.loads(json.dumps(context, default=lambda o: o.__dict__))

    for path, condition in dsl.items():
        value = get_by_path(context_dict, path)
        if isinstance(condition, dict):
            for op_key, op_value in condition.items():
                if op_key not in OP_MAP:
                    return False
                if isinstance(value, list):
                    if not any(OP_MAP[op_key](v, op_value) for v in value):
                        return False
                elif not OP_MAP[op_key](value, op_value):
                    return False
        else:
            if value != condition:
                return False

    return True
