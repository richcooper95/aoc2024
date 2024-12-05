import dataclasses

from collections import defaultdict
from typing import Dict, List, Set

from .. import utils

__all__ = ("main")


# Could probably remove this from Part A since we introduced the 'numbers_before' dict in
# Part B!
@dataclasses.dataclass
class Rule:
  first: int
  second: int

  def check(self, update: List[int]) -> bool:
    seen_first = False
    seen_second = False
    for item in update:
      if item == self.second:
        seen_second = True
        if seen_first:
          return True
      elif item == self.first:
        seen_first = True
        if seen_second:
          return False

    return True


@dataclasses.dataclass
class Update:
  items: List[int]

  def validate(self, rules: List[Rule]) -> bool:
    for rule in rules:
      if not rule.check(self.items):
        return False

    return True

  def reordered(self, numbers_before: Dict[int, Set[int]]) -> List[int]:
    new_order = [self.items[0]]
    for i in range(1, len(self.items)):
      item_to_insert = self.items[i]

      # Iterate through the new_order list until we find that the item to insert must come
      # before the item we're looking at in the new order (or we reach the end).
      j = 0
      while j < len(new_order) and item_to_insert not in numbers_before[new_order[j]]:
        j += 1
      new_order.insert(j, item_to_insert)
    return new_order


@utils.display
def validate(input_list: List[str]) -> int:
  sum_of_valid_middle_page_numbers = 0
  sum_of_invalid_middle_page_numbers = 0
  rules = []

  # Dict of int -> set(int) where the key is a number and the set contains all the numbers
  # that must come before it.
  numbers_before = defaultdict(set)

  for line in input_list:
    if "|" in line:
      first, second = map(int, line.split("|"))
      rules.append(Rule(first, second))
      numbers_before[second].add(first)
    elif line:
      # All the rules come first, so we have them all by this point.
      update = Update(list(map(int, line.split(","))))
      if update.validate(rules):
        sum_of_valid_middle_page_numbers += update.items[len(update.items) // 2]
      else:
        reordered_update = update.reordered(numbers_before)
        sum_of_invalid_middle_page_numbers += reordered_update[len(update.items) // 2]

  return sum_of_valid_middle_page_numbers, sum_of_invalid_middle_page_numbers


#---------------------------------------------------

def main() -> None:
  input_list = utils.get_input_list(__name__)
  validate(input_list)


if __name__ == "__main__":
  main()
