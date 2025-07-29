from typing import Any

__all__ = [
  "as_any",
  "ensure_tuple",
  "non_none",
]

def as_any(obj: Any) -> Any:
  return obj

def non_none[T](obj: T | None) -> T:
  assert obj is not None
  return obj

def ensure_tuple[T](value: T | tuple[T, ...]) -> tuple[T, ...]:
  return value if isinstance(value, tuple) else (value,)
