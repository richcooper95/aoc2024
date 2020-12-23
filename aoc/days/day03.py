from typing import List, Union
from math import prod
import dataclasses

from .. import utils

__all__ = ("main")


@dataclasses.dataclass
class Slope:
  x_inc: int = 3
  y_inc: int = 1
  x: int = 0
  y: int = 0
  trees: int = 0

  def __mul__(self, other: Union["Slope", int]):
    if isinstance(other, int):
      return self.trees * other
    elif isinstance(other, Slope):
      return self.trees * other.trees
    else:
      raise NotImplementedError
  
  def __rmul__(self, other: Union["Slope", int]):
    return self.__mul__(other)

  def increment(self) -> None:
    self.x += self.x_inc
    self.y += self.y_inc

  def is_tree(self, line: str) -> bool:
    return line[self.x % len(line)] == "#"

  def process_line(self, i: int, line: str) -> None:
    if i == self.y:
      if self.is_tree(line):
        self.trees += 1
      self.increment()


# O(N*S)
@utils.display
def count_trees(
  lines: List[str],
  slopes: List["Slope"]
) -> int:
  for i, line in enumerate(lines):
    for slope in slopes:
      slope.process_line(i, line)

  return prod(slopes)


#---------------------------------------------------

def main() -> None:
  input_list = utils.get_input_list(__name__)
  count_trees(input_list, [Slope(3, 1)]) # 225
  count_trees( # 1115775000
      input_list,
      [
        Slope(1, 1),
        Slope(3, 1),
        Slope(5, 1),
        Slope(7, 1),
        Slope(1, 2)
      ]
  )


if __name__ == "__main__":
  main()
