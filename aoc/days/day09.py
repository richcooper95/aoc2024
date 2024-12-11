import dataclasses

from collections import defaultdict
from typing import Dict, List, Set, Tuple

from .. import utils

__all__ = ("main")


def generate_blocks(input_string: str) -> str:
  blocks = ""
  file_length = True
  for _id, elem in enumerate(input_string):
    _id = _id // 2
    if file_length:
      blocks += str(_id) * int(elem)
      file_length = False
    else:
      blocks += "." * int(elem)
      file_length = True

  return blocks


def move_blocks(blocks: str) -> str:
  i = 0
  j = len(blocks) - 1
  new_blocks = ""
  end_dots = 0
  while i < len(blocks) and j >= i:
    if blocks[i] != ".":
      new_blocks += blocks[i]
      i += 1
    elif blocks[j] != ".":
      new_blocks += blocks[j]
      j -= 1
      i += 1
      end_dots += 1
    else:
      j -= 1
      end_dots += 1

  return new_blocks + "." * end_dots


def calculate_checksum(blocks: str) -> int:
  i = 0
  checksum = 0
  while i < len(blocks) and blocks[i] != ".":
    checksum += int(blocks[i]) * i
    i += 1

  return checksum


@utils.display
def process(input_string: str) -> int:
  blocks = generate_blocks(input_string)
  blocks = move_blocks(blocks)
  return calculate_checksum(blocks)

#---------------------------------------------------

def main() -> None:
  input_lines = utils.get_input_list(__name__)
  process(input_lines[0])


if __name__ == "__main__":
  main()
