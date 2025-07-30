from pathlib import Path
from typing import Any, Type

from pydantic_settings import BaseSettings


def _show(env_lines: list[str], save_path: Path | None = None):
    print("\n".join(env_lines))
    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text("\n".join(env_lines))
        print(f"Example file saved to {save_path}")


def _is_nested_settings(field: Any) -> bool:
    return isinstance(field, type) and issubclass(field, BaseSettings)


def show_settings_as_env(
    settings_obj: BaseSettings,
    save_path: Path | None = None,
):
    """Create a .env.example file with all settings fields."""

    env_lines = []

    def append_env_line(field_name: str, field: Any, parent_name: str = ""):
        if parent_name:
            env_line = f"{parent_name.upper()}_{field_name.upper()}={field}"
        else:
            env_line = f"{field_name.upper()}={field}"
        env_lines.append(env_line)

    def extend_env_lines(field_name: str, field: Any, parent_name: str = ""):
        """Create a .env.example file with all nested settings fields."""
        if _is_nested_settings(type(field)):
            for _field_name, _field in field.__dict__.items():
                extend_env_lines(_field_name, _field, field_name)
            env_lines.append("")
        else:
            append_env_line(field_name, field, parent_name)

    for field_name, field in settings_obj.__dict__.items():
        extend_env_lines(field_name, field)
    _show(env_lines, save_path)


def show_settings_as_env_example(
    settings_cls: Type[BaseSettings],
    save_path: Path | None = None,
):
    """Create a .env.example file with all settings fields."""

    env_lines = []

    def append_env_line(field_name: str, field: Any, parent_name: str = ""):
        if parent_name:
            env_line = f"{parent_name.upper()}_{field_name.upper()}={field.default}"
        else:
            env_line = f"{field_name.upper()}={field.default}"
        env_lines.append(env_line)

    def extend_env_lines(field_name: str, field: Any, parent_name: str = ""):
        """Create a .env.example file with all nested settings fields."""
        if _is_nested_settings(field.annotation):
            for _field_name, _field in field.annotation.model_fields.items():
                extend_env_lines(_field_name, _field, field_name)
            env_lines.append("")
        else:
            append_env_line(field_name, field, parent_name)

    for field_name, field in settings_cls.model_fields.items():
        extend_env_lines(field_name, field)
    _show(env_lines, save_path)
