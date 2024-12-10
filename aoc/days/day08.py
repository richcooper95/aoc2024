import dataclasses

from collections import defaultdict
from typing import Dict, List, Set, Tuple

from .. import utils

__all__ = ("main")


def get_antenna_locations(input_list: List[str]) -> Dict[str, List[Tuple[int, int]]]:
  antenna_locations = defaultdict(list)
  for i, line in enumerate(input_list):
    for j, cell in enumerate(line):
      if cell != ".":
        antenna_locations[cell].append((i, j))

  return antenna_locations


def get_antinodes(locations: List[Tuple[int, int]], i_max: int, j_max: int, *, all_antinodes: bool=False) -> Set[Tuple[int, int]]:
  antinodes = set()
  for i in range(len(locations)):
    for j in range(len(locations)):
      if i == j:
        continue

      delta = (locations[j][0] - locations[i][0], locations[j][1] - locations[i][1])

      first_antinode = (locations[i][0] - delta[0], locations[i][1] - delta[1])
      while 0 <= first_antinode[0] < i_max and 0 <= first_antinode[1] < j_max:
        antinodes.add(first_antinode)
        if not all_antinodes:
          break
        first_antinode = (first_antinode[0] + delta[0], first_antinode[1] + delta[1])

      second_antinode = (locations[j][0] + delta[0], locations[j][1] + delta[1])
      while 0 <= second_antinode[0] < i_max and 0 <= second_antinode[1] < j_max:
        antinodes.add(second_antinode)
        if not all_antinodes:
          break
        second_antinode = (second_antinode[0] + delta[0], second_antinode[1] + delta[1])

      if all_antinodes:
        antinodes.add(locations[i])
        antinodes.add(locations[j])

  return antinodes

@utils.display
def process(input_list: List[str], part: utils.Part) -> int:
  antinodes = set()
  for locations in get_antenna_locations(input_list).values():
    all_antinodes = part == utils.Part.B
    antinodes_for_location = get_antinodes(locations, len(input_list), len(input_list[0]), all_antinodes=all_antinodes)
    antinodes = antinodes.union(antinodes_for_location)

  return len(antinodes)


#---------------------------------------------------

def main() -> None:
  input_lines = utils.get_input_list(__name__)
  process(input_lines, utils.Part.A)
  process(input_lines, utils.Part.B)


if __name__ == "__main__":
  main()
