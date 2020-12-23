from typing import List, Tuple, Any
import dataclasses
import enum
import re
import time

from .. import utils

__all__ = ("main")


class InputSection(enum.IntEnum):
  RULES = 0
  MYTICKET = 1
  TICKETS = 2


SECTION_MARKERS = {
  "your ticket:": InputSection.MYTICKET,
  "nearby tickets:": InputSection.TICKETS,
}


@dataclasses.dataclass
class Range:
  min: int
  max: int

  def __contains__(self, num: int) -> bool:
    return self.min <= num <= self.max


  @classmethod
  def from_string(cls, string: str) -> "Range":
    return cls(*map(int, string.split("-")))


@dataclasses.dataclass
class Rule:
  name: str
  ranges: List[Range]

  def obeyed_by(self, num: int) -> bool:
    return any(num in range for range in self.ranges)


  @classmethod
  def from_string(cls, string: str) -> "Rule":
    match = re.fullmatch(r"([ \w]+): (\d+\-\d+) or (\d+\-\d+)", string)
    if match is not None:
      return cls(
        match[1],
        [Range.from_string(match[2]), Range.from_string(match[3])]
      )
    raise ValueError(f"Invalid rule string: {string}")


@dataclasses.dataclass
class Ticket:
  values: List[int]

  @classmethod
  def from_string(cls, string: str) -> "Ticket":
    return cls([int(val) for val in string.split(",")])


  def get_invalid_values(self, rules: List[Rule]) -> List[int]:
    invalid_values = []
    for val in self.values:
      if not any(rule.obeyed_by(val) for rule in rules):
        invalid_values.append(val)

    return invalid_values


def parse_input(input_list: List[str]) -> Tuple[Any]:
  section = InputSection.RULES
  rules = []
  valid_tickets = []
  invalid_count = 0

  for i, line in enumerate(input_list):
    if line:
      if line in SECTION_MARKERS:
        section = SECTION_MARKERS[line]

      elif section is InputSection.RULES:
        rules.append(Rule.from_string(line))

      elif section is InputSection.MYTICKET:
        my_ticket = Ticket.from_string(line)

      elif section is InputSection.TICKETS:
        ticket = Ticket.from_string(line)
        invalid_values = ticket.get_invalid_values(rules)

        for value in invalid_values:
          invalid_count += value

        if not invalid_values:
          valid_tickets.append(ticket)
  
  return rules, valid_tickets, my_ticket, invalid_count


@utils.display
def process(input_list: List[str]):
  start = time.monotonic()
  # Parse input (also obtaining the Part A result).
  rules, valid_tickets, my_ticket, invalid_count = parse_input(input_list)

  # Initially all slots could be for any rule.
  unknown_slots = {
    slot: set(range(len(rules))) for slot in range(len(rules))
  }

  print(f"{1000 * (time.monotonic() - start)}ms")
  
  # First use information from tickets to remove possible rule indices
  # if the rule is violated by any ticket values in that slot.
  for ticket in valid_tickets:
    for slot, val in enumerate(ticket.values):
      for rule_idx, rule in enumerate(rules):
        if not rule.obeyed_by(val):
          unknown_slots[slot].remove(rule_idx)

  print(f"{1000 * (time.monotonic() - start)}ms")

  # Next use information from already-determined fields to reach a final
  # assignment.
  known_slots = {}
  while len(known_slots) < len(rules):
    prev_len = len(known_slots)
    for slot, rule_idxs in unknown_slots.items():
      for name in known_slots.values():
        unknown_slots[slot].discard(name)

      if len(rule_idxs) == 1:
        known_slots[slot] = rule_idxs.pop()
    
    for slot in known_slots:
      if slot in unknown_slots:
        del unknown_slots[slot]

    if prev_len == len(known_slots):
      raise ValueError("Unable to uniquely determine fields.")

  print(f"{1000 * (time.monotonic() - start)}ms")
  
  prod = 1
  for slot, rule_idx in known_slots.items():
    if rules[rule_idx].name.startswith("departure"):
      prod *= my_ticket.values[slot]

  print(f"{1000 * (time.monotonic() - start)}ms")

  return invalid_count, prod


#---------------------------------------------------

def main() -> None:
  process(utils.get_input_list(__name__)) # 27911, 737176602479


if __name__ == "__main__":
  main()
