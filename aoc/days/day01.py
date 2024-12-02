from collections import Counter
from typing import List

from .. import utils

__all__ = ("main")


@utils.display
def difference(input_list: List[List[int]]) -> int:
  total = 0
  for i, j in zip(sorted(input_list[0]), sorted(input_list[1])):
    total += abs(i - j)

  return total

@utils.display
def similarity(input_list: List[List[int]]) -> int:
  counts = Counter(input_list[1])
  total = 0
  for i in input_list[0]:
    total += counts[i] * i

  return total

#---------------------------------------------------

def main() -> None:
  input_list = utils.get_split_input_list(__name__, cast_funcs=[int, int])
  difference(input_list)
  similarity(input_list)


if __name__ == "__main__":
  main()
