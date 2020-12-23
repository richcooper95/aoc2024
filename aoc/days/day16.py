from typing import List, Tuple, Any, Dict, Set
import dataclasses
import enum
import re

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


def parse_rules(lines: List[str]) -> List[Rule]:
  return [Rule.from_string(line) for line in lines]


def parse_tickets(
  lines: List[str],
  rules: List[Rule],
  unknown_slots: Dict[int, Set]
) -> int:
  invalid_count = 0
  for line in lines:
    ticket = Ticket.from_string(line)
    invalid_values = ticket.get_invalid_values(rules)

    for value in invalid_values:
      invalid_count += value

    if not invalid_values:
      # This ticket is valid, so use it to remove possible rules from the
      # unknown slots map if the associated rule is violated by any
      # ticket values in that slot.
      for slot, val in enumerate(ticket.values):
        for rule_idx, rule in enumerate(rules):
          if not rule.obeyed_by(val):
            unknown_slots[slot].remove(rule_idx)

  return invalid_count


@utils.display
def process(input_sections: List[str]):
  # Process the rules first, so we can use them while processing tickets.
  rules = parse_rules(input_sections[0].splitlines())

  # Initialise a map of each slot to the rule indices it could correspond to.
  # Initially, each slot could correspond to any rule index.
  unknown_slots = {
    slot: set(range(len(rules))) for slot in range(len(rules))
  }

  # Parse nearby tickets, obtaining the sum of all invalid values for Part A
  # and simultaneously reducing the unknown map for Part B.
  invalid_count = parse_tickets(
    input_sections[2].splitlines()[1:],
    rules,
    unknown_slots
  )

  # Next use information from already-determined fields to reach a known
  # assignment for each slot.
  known_slots = {}
  while len(known_slots) < len(rules):
    prev_len = len(known_slots)

    for slot, possible_rules in unknown_slots.items():
      for name in known_slots.values():
        unknown_slots[slot].discard(name)

      if len(possible_rules) == 1:
        known_slots[slot] = possible_rules.pop()
    
    for slot in known_slots:
      if slot in unknown_slots:
        del unknown_slots[slot]

    # Expect to assign a new known slot on each iteration. If we don't, then
    # we are unable to uniquely determine the slots.
    if prev_len == len(known_slots):
      raise ValueError("Unable to uniquely determine slots.")
  
  # Parse my ticket and calculate the product of all "departure*" fields.
  my_ticket = Ticket.from_string(input_sections[1].splitlines()[1].strip())

  prod = 1
  for slot, rule_idx in known_slots.items():
    if rules[rule_idx].name.startswith("departure"):
      prod *= my_ticket.values[slot]

  return invalid_count, prod


#---------------------------------------------------

def main() -> None:
  process(utils.get_input_sections(__name__)) # 27911, 737176602479


if __name__ == "__main__":
  main()
