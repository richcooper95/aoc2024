from typing import List, Set
from dataclasses import dataclass, field
import enum

from ..utils import get_input_list

__all__ = ("run")


def binary_search(data: str):
  i = 0
  start = 0
  end = 2 ** len(data) - 1
  while start != end:
    char = data[i]
    mid = (start + end) // 2
    if char in ["F", "L"]:
      end = mid
    elif char in ["B", "R"]:
      start = mid + 1
    i += 1

  return start


class Part(enum.IntEnum):
  A = 1
  B = 2


@dataclass
class Seat:
  id: int = 0
  occupied: bool = False


@dataclass
class Row:
  index: int = 0
  cols: List[bool] = field(
    default_factory=lambda: [Seat() for _ in range(8)]
  )


@dataclass
class Plane:
  rows: List[Row] = field(
    default_factory=lambda: [Row(i) for i in range(128)]
  )
  max_id: int = 0
  free_seat_ids: Set[int] = field(
    default_factory=lambda: set(
      x * 8 + y for x in range(128) for y in range(8)
    )
  )

  def decode_row(self, bpass_row: str):
    return binary_search(bpass_row)

  def decode_col(self, bpass_col: str):
    return binary_search(bpass_col)

  def add_pass(self, bpass: str):
    row = self.decode_row(bpass[:7])
    col = self.decode_col(bpass[7:])
    seat_id = row * 8 + col
    self.rows[row].cols[col].occupied = True
    self.rows[row].cols[col].id = seat_id
    self.free_seat_ids.remove(seat_id)
    self.max_id = max(seat_id, self.max_id)


def process(lines: List[str], part: Part) -> int:
  plane = Plane()
  for line in lines:
    plane.add_pass(line)

  if part is Part.A:
    return plane.max_id
  elif part is Part.B:
    for seat_id in plane.free_seat_ids:
      if all(x not in plane.free_seat_ids for x in [seat_id + 1, seat_id - 1]):
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
