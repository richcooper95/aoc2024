from typing import List, Callable, Any, Optional, IO

__all__ = (
  "get_input_list",
)

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
