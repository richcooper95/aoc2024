from typing import List, Any
import enum

from ..utils import get_input

__all__ = ("run")


class Part(enum.IntEnum):
  A = 1
  B = 2


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
    raise ValueError("Invalid part")

  return valid


def parsed_line(line: str) -> List[Any]:
  split_line = [z for x in line.split(":")
                  for y in x.strip().split()
                  for z in y.split("-")]
  split_line[0] = int(split_line[0])
  split_line[1] = int(split_line[1])

  return split_line


def check_lines(input: List[List[Any]], part: "Part") -> int:
  num_valid = 0

  for line in input:
    if check_valid(*line, part):
      num_valid += 1

  return num_valid

#--------------------------------------------------------------

def run_part_a() -> int: # 600
  return check_lines(get_input(2, cast_func=parsed_line), Part.A)


def run_part_b() -> int: # 245
  return check_lines(get_input(2, cast_func=parsed_line), Part.B)


def run() -> None:
  print(run_part_a())
  print(run_part_b())


if __name__ == "__main__":
  run()
