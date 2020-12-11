from typing import List, Callable, Any, Optional
from functools import wraps
import enum

__all__ = (
  "Part",
  "get_input_list",
  "memoize",
)


class Part(enum.IntEnum):
  A = 1
  B = 2


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

def memoize(func):
  cache = {}
  @wraps(func)
  def helper(*args):
    if args not in cache:
      cache[args] = func(*args)
    return cache[args]
  return helper
