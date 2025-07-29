from typing import Any, Callable, Iterable, overload
from .type_utils import as_any

__all__ = [
  "deepen_dict", "dict_by", "dict_firsts",
  "flatten_dict_inner", "flatten_dict",
  "get_at", "group",
  "key_of",
  "map_dict", "merge_dicts",
  "omit",
  "pick",
  "tuple_by",
]

def merge_dicts[T, K](*dicts: dict[K, T]) -> dict[K, T]:
  if len(dicts) == 1:
    return dicts[0]
  result = {}
  for d in dicts:
    result |= d
  return result

def omit[T, K](d: dict[K, T], keys: Iterable[K]) -> dict[K, T]:
  if keys:
    d = dict(d)
    for key in keys:
      del d[key]
  return d

def pick[T, K](d: dict[K, T], keys: Iterable[K]) -> dict[K, T]:
  return {key: d[key] for key in keys}

def dict_by[T, K](keys: Iterable[K], values: Iterable[T]) -> dict[K, T]:
  return dict(zip(keys, values))

def tuple_by[T, K](d: dict[K, T], keys: Iterable[K]) -> tuple[T, ...]:
  return tuple(d[key] for key in keys)

def map_dict[T, U, K](fn: Callable[[T], U], d: dict[K, T]) -> dict[K, U]:
  return {key: fn(value) for key, value in d.items()}

def key_of[T, U](dicts: Iterable[dict[T, U]], key: T) -> list[U]:
  return [d[key] for d in dicts]

def get_at[T](d: dict, keys: Iterable[Any], default: T) -> T:
  try:
    for key in keys:
      d = d[key]
  except KeyError:
    return default
  return as_any(d)

def dict_firsts[T, K](pairs: Iterable[tuple[K, T]]) -> dict[K, T]:
  result: dict[K, T] = {}
  for key, item in pairs:
    if key not in result:
      result[key] = item
  return result

def group[T, K](pairs: Iterable[tuple[K, T]]) -> dict[K, list[T]]:
  values_by_key = {}
  for key, value in pairs:
    values_by_key.setdefault(key, []).append(value)
  return values_by_key

@overload
def deepen_dict[K1, U](d: dict[tuple[K1], U]) -> dict[K1, U]: ...
@overload
def deepen_dict[K1, K2, U](d: dict[tuple[K1, K2], U]) -> dict[K1, dict[K2, U]]: ...
@overload
def deepen_dict[K1, K2, K3, U](d: dict[tuple[K1, K2, K3], U]) -> dict[K1, dict[K2, dict[K3, U]]]: ...
@overload
def deepen_dict[K1, K2, K3, K4, U](d: dict[tuple[K1, K2, K3, K4], U]) -> dict[K1, dict[K2, dict[K3, dict[K4, U]]]]: ...
@overload
def deepen_dict[K1, K2, K3, K4, K5, U](d: dict[tuple[K1, K2, K3, K4, K5], U]) -> dict[K1, dict[K2, dict[K3, dict[K4, dict[K5, U]]]]]: ...
@overload
def deepen_dict[K1, K2, K3, K4, K5, K6, U](d: dict[tuple[K1, K2, K3, K4, K5, K6], U]) -> dict[K1, dict[K2, dict[K3, dict[K4, dict[K5, dict[K6, U]]]]]]: ...
def deepen_dict(d: dict[tuple[Any, ...], Any]) -> dict:
  output = {}
  if () in d:
    return d[()]
  for (*tail, head), value in d.items():
    curr = output
    for key in tail:
      curr = curr.setdefault(key, {})
    curr[head] = value
  return output

def flatten_dict_inner(d, prefix=()):
  for key, value in d.items():
    if not isinstance(value, dict) or value == {}:
      yield prefix + (key,), value
    else:
      yield from flatten_dict_inner(value, prefix + (key,))

def flatten_dict(deep_dict: dict, prefix=()) -> dict:
  return dict(flatten_dict_inner(deep_dict, prefix))
