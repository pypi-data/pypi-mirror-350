import json
from pathlib import Path
from typing import Any

__all__ = [
  "read_json",
  "write_json",
]

default_sentinel = object()

def read_json(path: Path, default=default_sentinel) -> Any:
  if default is not default_sentinel and not path.exists():
    return default
  with path.open("r") as f:
    return json.load(f)

def write_json(path: Path, obj: object, indent: None | int = None) -> None:
  with path.open("w") as f:
    separators = (",", ":") if indent is None else None
    return json.dump(obj, f, indent=indent, separators=separators)
