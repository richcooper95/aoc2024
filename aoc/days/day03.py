import re

from typing import List, Optional

from .. import utils

__all__ = ("main")


@utils.display
def multiply(input_list: List[str]) -> int:
  matches = re.findall(r"mul\((\d+),(\d+)\)", str(input_list))
  return sum(int(x) * int(y) for x, y in matches)


@utils.display
def multiply_with_enabling(input_list: List[str]) -> int:
  input_string = "".join(str(x) for x in input_list)
  matches = re.findall(r"(do\(\)|don't\(\)|mul\(\d+,\d+\))", input_string)
  enabled = True
  result = 0
  for match in matches:
    if match == "do()":
      enabled = True
    elif match == "don't()":
      enabled = False
    elif enabled:
      x, y = re.match(r"mul\((\d+),(\d+)\)", match).groups()
      result += int(x) * int(y)

  return result


#---------------------------------------------------

def main() -> None:
  input_list = utils.get_input_list(__name__)
  multiply(input_list)
  multiply_with_enabling(input_list)


if __name__ == "__main__":
  main()
