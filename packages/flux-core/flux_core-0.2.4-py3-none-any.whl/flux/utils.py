from __future__ import annotations

import inspect
import json
import uuid
from datetime import datetime
from datetime import timedelta
from enum import Enum
from importlib import import_module as imodule
from importlib import util
from pathlib import Path
from types import GeneratorType
from typing import Any
from typing import Callable

from flux.errors import ExecutionError


def maybe_awaitable(func: Any | None) -> Any:
    if func is None:

        async def none_wrapper():
            return None

        return none_wrapper()

    if inspect.isawaitable(func):
        return func

    async def wrapper():
        return func

    return wrapper()


def make_hashable(item):
    if isinstance(item, dict):
        return tuple(sorted((k, make_hashable(v)) for k, v in item.items()))
    elif isinstance(item, list):
        return tuple(make_hashable(i) for i in item)
    elif isinstance(item, set):
        return frozenset(make_hashable(i) for i in item)
    elif type(item).__name__ == "pandas.DataFrame":
        return tuple(map(tuple, item.itertuples(index=False)))
    elif is_hashable(item):
        return item
    else:
        return str(item)


def is_hashable(obj) -> bool:
    try:
        hash(obj)
        return True
    except TypeError:
        return False


def to_json(obj):
    return json.dumps(obj, indent=4, cls=FluxEncoder)


def import_module(name: str) -> Any:
    return imodule(name)


def import_module_from_file(path: str) -> Any:
    file_path = Path(path)

    if file_path.is_dir():
        file_path = file_path / "__init__.py"
    elif file_path.suffix != ".py":
        raise ValueError(f"Invalid module path: {file_path}")

    spec = util.spec_from_file_location("workflow_module", file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot find module at {file_path}.")
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_value(value: str | None) -> Any:
    """Parse a string value into the correct Python type.

    Supports:
    - None, null, empty string -> None
    - true/false -> bool
    - integers -> int
    - floats -> float
    - valid JSON -> parsed JSON
    - everything else -> str

    Args:
        value: The value to parse

    Returns:
        The parsed value in its correct type
    """
    if value is None or value.lower() in ("none", "null") or value == "":
        return None

    if value.lower() == "true":
        return True

    if value.lower() == "false":
        return False

    if value.lower() == "nan":
        return float("nan")
    if value.lower() == "infinity" or value.lower() == "inf":
        return float("inf")
    if value.lower() == "-infinity" or value.lower() == "-inf":
        return float("-inf")

    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        pass

    try:
        return json.loads(value)
    except Exception as ex:  # noqa: F841
        pass

    return value


class FluxEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, datetime):
            return obj.isoformat()

        from flux import ExecutionContext

        if isinstance(obj, ExecutionContext):
            return {
                "name": obj.name,
                "execution_id": obj.execution_id,
                "input": obj.input,
                "output": obj.output,
                "state": obj.state,
                "events": obj.events,
            }

        if isinstance(obj, ExecutionError):
            obj = obj.inner_exception if obj.inner_exception else obj
            return {"type": type(obj).__name__, "message": str(obj)}

        if isinstance(obj, Exception):
            return {"type": type(obj).__name__, "message": str(obj)}

        if inspect.isclass(type(obj)) and isinstance(obj, Callable):
            return type(obj).__name__

        if isinstance(obj, Callable):
            return obj.__name__

        if isinstance(obj, GeneratorType):
            return str(obj)

        if isinstance(obj, timedelta):
            return obj.total_seconds()

        if isinstance(obj, uuid.UUID):
            return str(obj)

        if hasattr(obj, "__dict__"):
            return obj.__dict__

        return str(obj)
