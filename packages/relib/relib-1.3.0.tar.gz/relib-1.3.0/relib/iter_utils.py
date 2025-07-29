from itertools import chain
from typing import Any, Iterable, Literal, overload
from .dict_utils import dict_firsts

__all__ = [
  "distinct_by", "distinct", "drop_none",
  "first", "flatten",
  "intersect",
  "list_split",
  "move_value",
  "num_partitions",
  "reversed_enumerate",
  "sized_partitions", "sort_by",
  "transpose",
]

def first[T](iterable: Iterable[T]) -> T | None:
  return next(iter(iterable), None)

def drop_none[T](iterable: Iterable[T | None]) -> list[T]:
  return [x for x in iterable if x is not None]

def distinct[T](iterable: Iterable[T]) -> list[T]:
  return list(dict.fromkeys(iterable))

def distinct_by[T](pairs: Iterable[tuple[object, T]]) -> list[T]:
  return list(dict_firsts(pairs).values())

def sort_by[T](pairs: Iterable[tuple[Any, T]]) -> list[T]:
  pairs = sorted(pairs, key=lambda p: p[0])
  return [v for _, v in pairs]

def move_value[T](iterable: Iterable[T], from_i: int, to_i: int) -> list[T]:
  values = list(iterable)
  values.insert(to_i, values.pop(from_i))
  return values

def reversed_enumerate[T](values: list[T] | tuple[T, ...]) -> Iterable[tuple[int, T]]:
  return zip(reversed(range(len(values))), reversed(values))

def intersect[T](*iterables: Iterable[T]) -> list[T]:
  return list(set.intersection(*map(set, iterables)))

@overload
def flatten[T](iterable: Iterable[T], depth: Literal[0]) -> list[T]: ...
@overload
def flatten[T](iterable: Iterable[Iterable[T]], depth: Literal[1] = 1) -> list[T]: ...
@overload
def flatten[T](iterable: Iterable[Iterable[Iterable[T]]], depth: Literal[2]) -> list[T]: ...
@overload
def flatten[T](iterable: Iterable[Iterable[Iterable[Iterable[T]]]], depth: Literal[3]) -> list[T]: ...
@overload
def flatten[T](iterable: Iterable[Iterable[Iterable[Iterable[Iterable[T]]]]], depth: Literal[4]) -> list[T]: ...
@overload
def flatten(iterable: Iterable, depth: int) -> list: ...
def flatten(iterable: Iterable, depth: int = 1) -> list:
  for _ in range(depth):
    iterable = chain.from_iterable(iterable)
  return list(iterable)

def list_split[T](iterable: Iterable[T], sep: T) -> list[list[T]]:
  values = [sep, *iterable, sep]
  split_at = [i for i, x in enumerate(values) if x is sep]
  ranges = list(zip(split_at[0:-1], split_at[1:]))
  return [values[start + 1:end] for start, end in ranges]

def sized_partitions[T](values: Iterable[T], part_size: int) -> list[list[T]]:
  # "chunk"
  if not isinstance(values, list):
    values = list(values)
  num_parts = (len(values) / part_size).__ceil__()
  return [values[i * part_size:(i + 1) * part_size] for i in range(num_parts)]

def num_partitions[T](values: Iterable[T], num_parts: int) -> list[list[T]]:
  if not isinstance(values, list):
    values = list(values)
  part_size = (len(values) / num_parts).__ceil__()
  return [values[i * part_size:(i + 1) * part_size] for i in range(num_parts)]

@overload
def transpose[T1, T2](tuples: Iterable[tuple[T1, T2]], default_num_returns=0) -> tuple[list[T1], list[T2]]: ...
@overload
def transpose[T1, T2, T3](tuples: Iterable[tuple[T1, T2, T3]], default_num_returns=0) -> tuple[list[T1], list[T2], list[T3]]: ...
@overload
def transpose[T1, T2, T3, T4](tuples: Iterable[tuple[T1, T2, T3, T4]], default_num_returns=0) -> tuple[list[T1], list[T2], list[T3], list[T4]]: ...
@overload
def transpose[T1, T2, T3, T4, T5](tuples: Iterable[tuple[T1, T2, T3, T4, T5]], default_num_returns=0) -> tuple[list[T1], list[T2], list[T3], list[T4], list[T5]]: ...
@overload
def transpose[T](tuples: Iterable[tuple[T, ...]], default_num_returns=0) -> tuple[list[T], ...]: ...
def transpose(tuples: Iterable[tuple], default_num_returns=0) -> tuple[list, ...]:
  output = tuple(zip(*tuples))
  if not output:
    return ([],) * default_num_returns
  return tuple(map(list, output))
