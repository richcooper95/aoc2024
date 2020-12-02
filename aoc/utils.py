from typing import List, Callable, Any, Optional

__all__ = (
  "get_input",
)

def get_input(
  day: int,
  *,
  cast_func: Optional[Callable] = None
) -> List[Any]:
  cast_func = cast_func or (lambda x: x)
  with open(f"inputs/day{day:02d}.txt", "r") as f:
    return [cast_func(x) for x in f]
