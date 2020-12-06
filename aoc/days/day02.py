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
def check_lines(input: List[List[Any]], part: "Part") -> int:
  num_valid = 0

  for line in input:
    if check_valid(*line, part):
      num_valid += 1

  return num_valid

#---------------------------------------------------

def run_part_a() -> int: # 600
  return check_lines(get_input_list(2, cast_func=parsed_line), Part.A)


def run_part_b() -> int: # 245
  return check_lines(get_input_list(2, cast_func=parsed_line), Part.B)


def run() -> None:
  print(run_part_a())
  print(run_part_b())


if __name__ == "__main__":
  run()
