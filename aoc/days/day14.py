from typing import Dict, List
import re

from .. import utils

__all__ = ("main")


class Computer:
  MASK_LEN = 36

  def __init__(self, init_prog: List[str], part: utils.Part):
    self.init_prog = init_prog
    self.part = part
    self.mask = "X" * self.MASK_LEN
    self.memory: Dict[int, int] = dict()

  def init(self):
    for line in self.init_prog:
      match = re.fullmatch(r"mask = ([X01]+)", line)
      if match is not None:
        # Update the mask.
        self.mask = match[1]
        if len(self.mask) != self.MASK_LEN:
          raise ValueError(f"Invalid length mask: {self.mask}")
      else:
        match = re.fullmatch(r"mem\[(\d+)\] = (\d+)", line)
        if match is not None:
          # Write the value to memory in the given location.
          self.write(int(match[1]), int(match[2]), self.part)

    return sum(self.memory.values())

  
  def write(self, loc: int, val: int, part: utils.Part):
    def _get_locs(masked_loc: str):
      # Recursively obtain a list of all memory locations by
      # replacing floating bits with 0 or 1.
      for char in masked_loc:
        if char == "X":
          # Recurse down both branches: replacing X with 0, and
          # replacing X with 1. Sum the two lists.
          return (
            _get_locs(masked_loc.replace("X", "0", 1)) +
            _get_locs(masked_loc.replace("X", "1", 1))
          )
      # No more X's in the string, so return a list containing
      # the string. We've reached the bottom of the call tree.
      return [masked_loc]

    if part is utils.Part.A:
      masked_val = "".join([
        v if m == "X" else m
        for m, v in zip(self.mask, f"{val:0{self.MASK_LEN}b}")
      ])
      self.memory[loc] = int(masked_val, 2)
    elif part is utils.Part.B:
      masked_loc = "".join([
        l if m == "0" else m
        for m, l in zip(self.mask, f"{loc:0{self.MASK_LEN}b}")
      ])
      for _loc in _get_locs(masked_loc):
        self.memory[int(_loc)] = val
    else:
      raise ValueError("Invalid part.")


@utils.display
def process(input_list: List[str], part: utils.Part):
  computer = Computer(input_list, part)

  return computer.init()


#---------------------------------------------------

def main() -> None:
  input_list = utils.get_input_list(__name__)
  process(input_list, utils.Part.A) # 13476250121721
  process(input_list, utils.Part.B) # 4463708436768


if __name__ == "__main__":
  main()
