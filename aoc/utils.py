from typing import List, Callable, Any, Optional
from functools import wraps
import enum
import time

__all__ = (
  "Part",
  "get_input_list",
  "memoize",
)


class Part(enum.IntEnum):
  A = 1
  B = 2


def print_tdelta(start: int):
  print(f"{1000 * (time.monotonic() - start):.3f}ms")


def get_input_list(
  module: str,
  *,
  cast_func: Optional[Callable] = None,
  test: Optional[bool] = False
) -> List[Any]:
  cast_func = cast_func or (lambda x: x)
  test_dir = "test/" if test else ""
  day = module.split(".")[-1]
  with open(f"inputs/{test_dir}{day}.txt", "r") as f:
    return [cast_func(x.strip()) for x in f]

def get_split_input_list(
  module: str,
  *,
  cast_funcs: Optional[List[Callable]] = None,
  test: Optional[bool] = False
) -> List[List[Any]]:
  """
  Read the input file and return a list of lists of the input elements.

  Args:
    module: The module name.
    cast_funcs: A list of functions to cast the input elements to. Must be the
      same length as the number of elements in each line.
    test: Whether to read the test input file.

  Returns:
    A list of lists of the input elements, cast to the appropriate types.
  """
  test_dir = "test/" if test else ""
  day = module.split(".")[-1]
  with open(f"inputs/{test_dir}{day}.txt", "r") as f:
    num_elements = len(f.readline().split())
    f.seek(0)

    if cast_funcs is None:
      return [line.split() for line in f]

    if len(cast_funcs) != num_elements:
      raise ValueError(
        f"Number of cast functions ({len(cast_funcs)}) must match the number of "
        f"elements in each line ({num_elements})."
      )

    values = [[] for _ in range(num_elements)]
    for line in f:
      for i, cast_func in enumerate(cast_funcs):
        values[i].append(cast_func(line.split()[i]))

    return values


def get_input_sections(
  module: str,
  *,
  test: Optional[bool] = False
) -> List[Any]:
  test_dir = "test/" if test else ""
  day = module.split(".")[-1]
  with open(f"inputs/{test_dir}{day}.txt", "r") as f:
    return f.read().split("\n\n")


def memoize(func: Callable):
  cache = {}
  @wraps(func)
  def helper(*args):
    if args not in cache:
      cache[args] = func(*args)
    return cache[args]
  return helper


def display(func: Callable):
  @wraps(func)
  def helper(*args, **kwargs):
    start = time.monotonic()
    result = func(*args, **kwargs)
    end = time.monotonic()
    t_delta = f"({1000 * (end - start):.3f}ms)"
    if isinstance(result, tuple):
      print(", ".join([str(x) for x in result]), t_delta)
    elif result is not None:
      print(result, t_delta)
    return result
  return helper
