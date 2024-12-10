from collections import defaultdict

import copy
from typing import List, Optional, Tuple

from .. import utils

__all__ = ("main")


OBSTACLE = "#"
GUARD_UP = "^"
GUARD_DOWN = "v"
GUARD_LEFT = "<"
GUARD_RIGHT = ">"

NEXT_GUARD = {
  GUARD_UP: GUARD_RIGHT,
  GUARD_RIGHT: GUARD_DOWN,
  GUARD_DOWN: GUARD_LEFT,
  GUARD_LEFT: GUARD_UP
}


class Area:
  def __init__(self, grid: List[str]) -> None:
    self.guard: str = GUARD_UP
    self.guard_initial_state: Tuple[int, int, str] = (0, 0, GUARD_UP)
    self.obstacle_indices = set()
    self.seen_indices = defaultdict(list)
    self.grid_size = (len(grid), len(grid[0]))
    self.loop_locations = set()

    for i, row in enumerate(grid):
      for j, cell in enumerate(row):
        if cell in NEXT_GUARD:
          print(f"Guard {cell} found at ({i}, {j})")
          self.guard_initial_state = (i, j, cell)
          self.guard = cell
          self.seen_indices[(i, j)].append(cell)
        elif cell == OBSTACLE:
          self.obstacle_indices.add((i, j))

  def move_guard(self) -> int:
    i, j, _ = self.guard_initial_state
    while True:
      # self.print()

      # if input("Press Enter to continue, or 'q' to quit: ") == "q":
      #   break

      test_i, test_j = self.take_step(i, j)

      if self.is_obstacle(test_i, test_j):
        # print(f"Guard {self.guard} has found an obstacle at ({test_i}, {test_j})")
        self.rotate_guard()
        # print(f"Guard has rotated to {self.guard}")
        continue

      if not self.in_bounds(test_i, test_j):
        # print(f"Guard has left the area at ({i}, {j})")
        return len(self.seen_indices), len(self.loop_locations)

      # Check whether, if we rotated the guard, it would ever enter a path it has already
      # visited.
      check_guard = self.rotated_guard(self.guard)
      check_i, check_j = i, j
      check_seen_indices = defaultdict(list)
      while self.in_bounds(check_i, check_j):
        if self.is_obstacle(check_i, check_j):
          # print(f"  Guard {check_guard} has found an obstacle at ({check_i}, {check_j})")
          check_guard = self.rotated_guard(check_guard)
          # print(f"  Guard has rotated to {check_guard}")
          check_i, check_j = self.take_step(check_i, check_j, guard=check_guard)
          continue

        if (
          check_guard in check_seen_indices[(check_i, check_j)]
          or check_guard in self.seen_indices[(check_i, check_j)]
        ):
          # print(f"Adding an obstacle at {(test_i, test_j)} would cause a loop")
          if (test_i, test_j) != self.guard_initial_state[:2]:
            self.loop_locations.add((test_i, test_j))
          break

        check_seen_indices[(check_i, check_j)].append(check_guard)
        check_i, check_j = self.take_step(check_i, check_j, guard=check_guard)
        # print(f"  Guard has moved to ({check_i}, {check_j})")

      # If we get here, we know:
      # 1. The next step for the guard is not an obstacle.
      # 2. The next step for the guard is in bounds.

      # Add the current position to the seen indices and move the guard.
      self.seen_indices[(test_i, test_j)].append(self.guard)

      # print(f"Guard has moved to ({test_i}, {test_j})")
      i = test_i
      j = test_j

  def print(self) -> None:
    for i in range(self.grid_size[0]):
      for j in range(self.grid_size[1]):
        if (i, j) in self.obstacle_indices:
          print(OBSTACLE, end="")
        elif (i, j) in self.seen_indices:
          print(self.seen_indices[(i, j)][-1], end="")
        else:
          print(".", end="")
      print()

  def in_bounds(self, i: int, j: int) -> bool:
    return 0 <= i < self.grid_size[0] and 0 <= j < self.grid_size[1]

  def take_step(self, i: int, j: int, *, guard: Optional[str]=None) -> Tuple[int, int]:
    if guard is None:
      guard = self.guard

    if guard == GUARD_UP:
      return i - 1, j

    if guard == GUARD_DOWN:
      return i + 1, j

    if guard == GUARD_LEFT:
      return i, j - 1

    if guard == GUARD_RIGHT:
      return i, j + 1

  def rotate_guard(self) -> None:
    self.guard = self.rotated_guard(self.guard)

  @staticmethod
  def rotated_guard(guard: str) -> str:
    return NEXT_GUARD[guard]

  def is_obstacle(self, i: int, j: int) -> bool:
    return (i, j) in self.obstacle_indices


@utils.display
def walk(input_list: List[str]) -> int:
  area = Area(input_list)
  return area.move_guard()


#---------------------------------------------------

def main() -> None:
  input_list = utils.get_input_list(__name__)
  walk(input_list)


if __name__ == "__main__":
  main()
