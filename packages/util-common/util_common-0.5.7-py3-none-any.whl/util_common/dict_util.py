from typing import Any


def values_to_str(data: dict[Any, Any], recursive: bool = False):
    if recursive:
        return {
            k: values_to_str(v, True) if isinstance(v, dict) else str(v) for k, v in data.items()
        }
    return {k: str(v) for k, v in data.items()}


def add_fields(data: dict[Any, Any], new_fields: dict[Any, Any]):
    for key, value in new_fields.items():
        if key not in data:
            data[key] = value
    return data
