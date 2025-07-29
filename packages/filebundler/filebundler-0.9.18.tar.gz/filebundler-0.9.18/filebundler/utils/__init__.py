# filebundler/utils/__init__.py
import io
import json
import logging

from pathlib import Path
from datetime import date, datetime
from typing import Any, Optional, Type, TypeVar, Union

from pydantic import BaseModel as PydanticBaseModel


logger = logging.getLogger(__name__)


def format_datetime(dt: Optional[Union[datetime, date]]):
    """Format datetime for display"""
    if not dt:
        return "Never"
    return dt.strftime("%Y-%m-%d %H:%M")


class BaseModel(PydanticBaseModel):
    pass


def json_dump(data: Any, f: io.TextIOWrapper):
    json.dump(data, f, indent=4)


def json_load(f: io.TextIOWrapper) -> Any:
    try:
        return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"JSONDecodeError: {e}")
        return None


def read_file(file_path: Path):
    assert file_path.exists(), f"Can't read file {file_path} because it doesn't exist"

    try:
        return file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        logger.error(f"UnicodeDecodeError for {file_path.name}: {e}")
        return f"Could not read {file_path.name} as text. It may be a binary file."


def dump_model_to_file(model: BaseModel, file_path: Path):
    file_path.write_bytes(model.model_dump_json(indent=4).encode("utf-8"))


T = TypeVar("T", bound=BaseModel)


def load_model_from_file(model_class: Type[T], file_path: Path):
    file_data = read_file(file_path)
    return model_class.model_validate_json(file_data)
