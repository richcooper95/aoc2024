from typing import List, Any
import re

from ..utils import get_input_list, Part

__all__ = ("run")


def check_valid(
  i: int,
  j: int,
  char: str,
  pword: str,
  part: "Part"
) -> bool:
  if part is Part.A:
    valid = pword.count(char) in range(i, j + 1)
  elif part is Part.B:
    valid = (pword[i - 1] == char) ^ (pword[j - 1] == char)
  else:
    raise ValueError("Invalid part.")

  return valid


def parsed_line(line: str) -> List[Any]:
  match = re.match(r"(\d+)-(\d+) (\w)\: (\w+)", line)

  if match is None:
    raise ValueError("Line does not match expected format.")

  return int(match[1]), int(match[2]), match[3], match[4]


# O(N)
def process(input: List[List[Any]]) -> int:
  count_a = 0
  count_b = 0

  for line in input:
    if check_valid(*line, Part.A):
      count_a += 1
    if check_valid(*line, Part.B):
      count_b += 1

  return count_a, count_b

#---------------------------------------------------

def run() -> None:
  res_a, res_b = process(get_input_list(2, cast_func=parsed_line))
  print(res_a) # 600
  print(res_b) # 245


if __name__ == "__main__":
  run()
