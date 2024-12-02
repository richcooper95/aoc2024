from typing import List, Optional

from .. import utils

__all__ = ("main")


@utils.display
def safety_test(input_list: List[List[int]]) -> int:
  safe_count = 0
  for line in input_list:
    if line_safe(line):
      safe_count += 1

  return safe_count

@utils.display
def safety_test_with_dampener(input_list: List[List[int]]) -> int:
  # TODO: We might be able to do something clever here around caching, to avoid
  # recalculating whether the same parts of a line are safe multiple times. Not sure
  # I can be bothered, though!
  safe_count = 0
  for line in input_list:
      if line_safe(line):
        safe_count += 1
      else:
        for i in range(len(line)):
          if line_safe(line, idx_to_remove=i):
            safe_count += 1
            break

  return safe_count

def line_safe(line: List[int], *, idx_to_remove: Optional[int]=None) -> bool:
  if idx_to_remove is not None:
    line = line[:idx_to_remove] + line[idx_to_remove + 1:]

  ascending = True
  for i in range(len(line)):
    if i == 0:
      continue

    if i == 1:
      if not 0 < abs(line[i] - line[i - 1]) < 4:
        return False

      ascending = line[i] > line[i - 1]

    if (
      (line[i] <= line[i - 1] and ascending)
      or (line[i] >= line[i - 1] and not ascending)
      or not 0 < abs(line[i] - line[i - 1]) < 4):
      return False

  return True

def parse_line(line: str) -> List[int]:
  return list(map(int, line.split()))


#---------------------------------------------------

def main() -> None:
  input_list = utils.get_input_list(__name__, cast_func=parse_line)
  safety_test(input_list)
  safety_test_with_dampener(input_list)


if __name__ == "__main__":
  main()
