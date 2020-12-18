from typing import List
import dataclasses
import enum
import numpy as np
import re

from .. import utils

__all__ = ("main")


class Compass(enum.Enum):
  NORTH = "N"
  EAST = "E"
  SOUTH = "S"
  WEST = "W"


@dataclasses.dataclass
class Ship:
  position: np.ndarray
  part: utils.Part
  orientation: Compass = Compass.EAST
  waypoint: np.ndarray = None

  @property
  def manhattan(self):
    return sum(abs(x) for x in self.position)


  def move_forward(self, val: int):
    if self.part is utils.Part.A:
      {
        Compass.NORTH: self.move_north,
        Compass.EAST: self.move_east,
        Compass.SOUTH: self.move_south,
        Compass.WEST: self.move_west
      }.get(self.orientation)(val)
    elif self.part is utils.Part.B:
      self.position += self.waypoint * val


  def move_north(self, val: int):
    if self.part is utils.Part.A:
      self.position[1] += val
    elif self.part is utils.Part.B:
      self.waypoint[1] += val


  def move_south(self, val: int):
    if self.part is utils.Part.A:
      self.position[1] -= val
    elif self.part is utils.Part.B:
      self.waypoint[1] -= val


  def move_east(self, val: int):
    if self.part is utils.Part.A:
      self.position[0] += val
    elif self.part is utils.Part.B:
      self.waypoint[0] += val


  def move_west(self, val: int):
    if self.part is utils.Part.A:
      self.position[0] -= val
    elif self.part is utils.Part.B:
      self.waypoint[0] -= val


  def turn_right(self, deg: int):
    if self.part is utils.Part.A:
      dirs = [Compass.NORTH, Compass.EAST, Compass.SOUTH, Compass.WEST]
      self.orientation = dirs[
        (dirs.index(self.orientation) + int(deg / 90)) % len(dirs)
      ]
    elif self.part is utils.Part.B:
      rad = np.deg2rad(deg)
      cos = np.cos(rad)
      sin = np.sin(rad)
      self.waypoint = np.array([
        int(cos * self.waypoint[0]) + int(sin * self.waypoint[1]),
        int(-sin * self.waypoint[0]) + int(cos * self.waypoint[1])
      ])
  

  def turn_left(self, deg: int):
    self.turn_right(-deg)


  def process_instruction(self, char: str, val: int):
    {
      "N": self.move_north,
      "E": self.move_east,
      "S": self.move_south,
      "W": self.move_west,
      "L": self.turn_left,
      "R": self.turn_right,
      "F": self.move_forward
    }[char](val)


  def travel(self, instructions: List[str]):
    for instruction in instructions:
      match = re.fullmatch(r"([NSEWLRF])(\d+)", instruction)
  
      if match is None:
        raise ValueError(f"Invalid instruction: {instruction}")

      self.process_instruction(match[1], int(match[2]))


def process(part: utils.Part):
  ship = Ship(
    np.array([0, 0]),
    part,
    waypoint=np.array([10, 1]) if part is utils.Part.B else None
  )

  ship.travel(utils.get_input_list(__name__))
  
  return ship.manhattan


#---------------------------------------------------

def main() -> None:
  print(process(utils.Part.A)) # 998
  print(process(utils.Part.B)) # 71586


if __name__ == "__main__":
  main()
