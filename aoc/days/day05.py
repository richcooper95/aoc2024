from typing import List, Set
from dataclasses import dataclass, field
import math
import re

from ..utils import get_input_list, Part

__all__ = ("run")

NUM_ROWS = 128
NUM_COLS = 8
NUM_ROW_INSTRUCTIONS = int(math.log(NUM_ROWS, 2))
NUM_COL_INSTRUCTIONS = int(math.log(NUM_COLS, 2))


# (C) Debbie Martin 2020 - cool bitwise solution
def binary_search_bits(instructions: str, left_char: str, right_char: str):
  """Use bitwise ops to find the index from the instructions.

  Think of "finding a number in [0, 127]" as adding a series of powers of 2
  to move you along the numberline. The powers of 2 you add are dictated by
  which half you take on each iteration:
    - If taking the right half of the remaining series, then add the power
      of 2 which takes you to the first value of the right half from your
      starting value.
    - If taking the left half, then don't add anything.

  E.g. consider the range [0, 7] as a toy example, and say we're given RLR.
  The pattern to find the index (5) would be:
      0 1 2 3 4 5 6 7   << starting series (val = 0)
              4 5 6 7   << take right half - add 2^2 = 4 to val (val = 4)
              4 5       << take left half (val = 4)
                5       << take right half - add 2^0 = 1 to val (val = 5)

  The power of 2 to add is determined by a bitwise left-shift of 1 - c.f.
    0001 = 1
    0010 = 2
    0100 = 4
    1000 = 8

  Cool!
  """
  val = 0
  for i in range(len(instructions)):
    if instructions[i] == right_char:
      val += 1 << (len(instructions) - i - 1) # add the right power of 2
  return val


def binary_search(instructions: str, left_char: str, right_char: str):
  """Use a binary search to find the index from the instructions."""
  i = 0
  start = 0
  end = 2 ** len(instructions) - 1
  while start != end:
    char = instructions[i]
    mid = (start + end) // 2
    if char == left_char:
      end = mid
    elif char == right_char:
      start = mid + 1
    i += 1

  return start


@dataclass
class Plane:
  seat_ids: Set[int] = field(
    default_factory=lambda: set()
  )
  min_id: int = 0
  max_id: int = 0

  def add_pass(self, bpass: str):
    match = re.fullmatch(r"([FB]{7})([LR]{3})", bpass)
    if match is None:
      raise ValueError("Boarding pass not in expected format.")

    row = binary_search(match[1], "F", "B")
    col = binary_search(match[2], "L", "R")

    seat_id = row * NUM_COLS + col

    self.seat_ids.add(seat_id)
    self.max_id = max(seat_id, self.max_id)
    self.min_id = min(seat_id, self.min_id) if self.min_id != 0 else seat_id


def process(lines: List[str], part: Part) -> int:
  plane = Plane()
  for line in lines:
    plane.add_pass(line)

  if part is Part.A:
    return plane.max_id
  elif part is Part.B:
    for seat_id in range(plane.min_id, plane.max_id):
      if seat_id not in plane.seat_ids:
        return seat_id
  else:
    raise ValueError("Invalid part.")
  

#---------------------------------------------------

def run_part_a() -> int: # 944
  return process(get_input_list(5), Part.A)


def run_part_b() -> int: # 554
  return process(get_input_list(5), Part.B)


def run() -> None:
  print(run_part_a())
  print(run_part_b())


if __name__ == "__main__":
  run()
