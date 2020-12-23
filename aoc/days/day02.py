from typing import List, Any
import re

from .. import utils

__all__ = ("main")


def check_valid(
  i: int,
  j: int,
  char: str,
  pword: str,
  part: "utils.Part"
) -> bool:
  if part is utils.Part.A:
    valid = pword.count(char) in range(i, j + 1)
  elif part is utils.Part.B:
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
@utils.display
def process(input: List[List[Any]]) -> int:
  count_a = 0
  count_b = 0

  for line in input:
    if check_valid(*line, utils.Part.A):
      count_a += 1
    if check_valid(*line, utils.Part.B):
      count_b += 1

  return count_a, count_b

#---------------------------------------------------

def main() -> None:
  process(utils.get_input_list(__name__, cast_func=parsed_line)) # 600, 245


if __name__ == "__main__":
  main()
