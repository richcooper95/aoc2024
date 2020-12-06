from typing import List, Callable, Any, Optional, IO
import enum

__all__ = (
  "get_input_list",
  "Part",
)


class Part(enum.IntEnum):
  A = 1
  B = 2


def get_input_list(
  day: int,
  *,
  cast_func: Optional[Callable] = None,
  test: Optional[bool] = False
) -> List[Any]:
  cast_func = cast_func or (lambda x: x)
  test_dir = "test/" if test else ""
  with open(f"inputs/{test_dir}day{day:02d}.txt", "r") as f:
    return [cast_func(x.strip()) for x in f]
