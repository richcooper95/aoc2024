from typing import List, Tuple
import enum
import re

from ..utils import get_input_list

__all__ = ("run")


class InvalidInstructionsError(Exception):
  pass


class InstructionOutOfRangeError(InvalidInstructionsError):
  pass


class InfiniteLoopError(InvalidInstructionsError):
  pass


class Command(enum.IntEnum):
  NOP = 0
  ACC = 1
  JMP = 2


class Console:
  def __init__(self, instructions: List[str]) -> None:
    self.instructions = instructions
    self.accumulator = 0
    self.next = 0
    self.visited = set()
  
  @property
  def booted(self) -> bool:
    return self.next == len(self.instructions)

  def boot(self):
    while not self.booted:
      self.process_instruction(self.next)


  def parse_line(self, instruction: str):
    match = re.fullmatch(
      r"(?P<cmd>{cmd_vals}) (?P<incr>(?:\-|\+)\d+)".format(
        cmd_vals="|".join([s.lower() for s in Command._member_names_])
      ),
      instruction
    )
    if match is None:
      raise InvalidInstructionsError(
        f"Instruction '{instruction}' is invalid."
      )

    return Command[match.group("cmd").upper()], int(match.group("incr"))
  
  def process_instruction(self, lineno: int):
    try:
      cmd, incr = self.parse_line(self.instructions[lineno])
    except IndexError as exc:
      raise InstructionOutOfRangeError(
        f"Index {lineno} out of range (max: {len(self.instructions) - 1})."
      ) from exc

    if cmd is Command.NOP:
      self.next = lineno + 1
    elif cmd is Command.ACC:
      self.accumulator += incr
      self.next = lineno + 1
    elif cmd is Command.JMP:
      self.next = lineno + incr
    else:
      raise ValueError("Invalid command.")

    if self.next in self.visited:
      raise InfiniteLoopError

    self.visited.add(lineno)


def process(lines: List[str]) -> Tuple[int]:
  console = Console(lines)
  try:
    console.boot()
  except InfiniteLoopError:
    acc_before_loop = console.accumulator

  # Try swapping "nop" and "jmp" in each line until we successfully boot.
  # (C) Martin Henstridge: We know the faulty line has been visited, so only
  #     need to iterate through those lines!
  cmd_map = {"nop": "jmp", "jmp": "nop"}
  visited = console.visited
  for idx in visited:
    cmd, incr = lines[idx].split()
    if cmd in cmd_map:
      lines[idx] = " ".join([cmd_map[cmd], incr])
      console = Console(lines)
      try:
        console.boot()
      except (InfiniteLoopError, InstructionOutOfRangeError):
        lines[idx] = " ".join([cmd, incr])
      else:
        acc_success = console.accumulator
        break

  return acc_before_loop, acc_success
  

#---------------------------------------------------

def run() -> None:
  res_a, res_b = process(get_input_list(8))
  print(res_a) # 1941
  print(res_b) # 2096


if __name__ == "__main__":
  run()
