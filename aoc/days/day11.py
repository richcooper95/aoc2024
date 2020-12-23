from typing import List, Any
import dataclasses
import enum

from .. import utils

__all__ = ("main")


class State(enum.Enum):
  FLOOR = "."
  EMPTY = "L"
  OCCUPIED = "#"


class BoundedList(list):
  def __getitem__(self, idx: int) -> Any:
    if idx < 0:
      raise IndexError
    return list.__getitem__(self, idx)


@dataclasses.dataclass
class Space:
  state: State
  checked_spaces: List["Space"] = None
  new_state = None
  
  def __repr__(self) -> str:
    return str(self.state)


  def calculate_new_state(self, part: utils.Part) -> None:
    if part is utils.Part.A:
      num = 4
    elif part is utils.Part.B:
      num = 5
    else:
      raise ValueError("Invalid part.")
    
    if (
      self.state is State.EMPTY
      and all(s.state in [State.FLOOR, State.EMPTY] for s in self.checked_spaces)
    ):
      self.new_state = State.OCCUPIED
    elif (
      self.state is State.OCCUPIED
      and len([s for s in self.checked_spaces if s.state is State.OCCUPIED]) >= num
    ):
      self.new_state = State.EMPTY
    else:
      self.new_state = self.state


  def update(self) -> None:
    self.state = self.new_state


class Row:
  def __init__(self, spaces):
    self.spaces = spaces


  def __getitem__(self, idx: int):
    if idx < 0:
      raise IndexError
    return self.spaces[idx]


  def __len__(self):
    return len(self.spaces)


  @classmethod
  def from_string(cls, string: str):
    return cls([Space(State(item)) for item in string])


@dataclasses.dataclass
class Ferry:
  rows: BoundedList = dataclasses.field(
    default_factory=lambda: BoundedList()
  )

  def __repr__(self):
    string = ""
    for row in self.rows:
      string += "\n" + "".join(space.state.value for space in row)
    return string


  @property
  def x_max(self):
    return len(self.rows[0]) - 1


  @property
  def y_max(self):
    return len(self.rows) - 1


  def update(self, part: utils.Part):
    # first pass calculates new state based on current state
    occupied = 0
    changed = False
    for y, row in enumerate(self.rows):
      for x, space in enumerate(row):
        # set the spaces to check if not already set
        if space.checked_spaces is None:
          space.checked_spaces = self.get_checked_spaces(part, x, y)
  
        space.calculate_new_state(part)

        if not changed:
          changed = space.state != space.new_state

        occupied += 1 if space.state is State.OCCUPIED else 0
  
    # second pass enacts the state update for each space
    for row in self.rows:
      for space in row:
        space.update()
  
    return occupied, changed


  @staticmethod
  def _get_neighbour_indices(x: int, y: int):
    return [
      (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
      (x - 1, y), (x + 1, y),
      (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
    ]


  def _get_visible_seat(self, x: int, y: int, dx: int, dy: int):
    _x = x + dx
    _y = y + dy
    while 0 <= _x <= self.x_max and 0 <= _y <= self.y_max:
      space = self.rows[_y][_x]
      if space.state is not State.FLOOR:
        return space
      _x += dx
      _y += dy


  def _get_visible_seats(self, x: int, y: int):
    seats = []
    deltas = [
      (0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1),
    ]
    for dx, dy in deltas:
      seat = self._get_visible_seat(x, y, dx, dy)
      if seat is not None:
        seats.append(seat)
    return seats


  def get_checked_spaces(self, part: utils.Part, x: int, y: int):
    checked_spaces = []
    if part is utils.Part.A:
      for _x, _y in self._get_neighbour_indices(x, y):
        try:
          checked_spaces.append(self.rows[_y][_x])
        except IndexError:
          pass
    elif part is utils.Part.B:
      checked_spaces = [seat for seat in self._get_visible_seats(x, y)]
    else:
      raise ValueError("Invalid part.")
    
    return checked_spaces


@utils.display
def process(part: utils.Part):
  ferry = Ferry(
    BoundedList(
      utils.get_input_list(__name__, cast_func=Row.from_string)
    )
  )

  changed = True
  while changed:
    occupied, changed = ferry.update(part)

  return occupied


#---------------------------------------------------

def main() -> None:
  process(utils.Part.A) # 2270
  process(utils.Part.B) # 2042


if __name__ == "__main__":
  main()
