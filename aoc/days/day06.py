from typing import List, Tuple

from ..utils import get_input_list

__all__ = ("run")


def process(lines: List[str]) -> Tuple[int]:
  i = 0
  count_a = 0
  count_b = 0
  while i < len(lines):
    group = []
    while i < len(lines) and lines[i]:
      group.append(set(lines[i]))
      i += 1
    count_a += len(group[0].union(*group[1:]))
    count_b += len(group[0].intersection(*group[1:]))
    i += 1

  return count_a, count_b
  

#---------------------------------------------------

def run() -> None:
  res_a, res_b = process(get_input_list(6))
  print(res_a) # 6532
  print(res_b) # 3427


if __name__ == "__main__":
  run()
