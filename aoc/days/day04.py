from typing import List, ClassVar, Optional, Callable, Mapping
import dataclasses
import enum
from functools import partial
import re

from ..utils import get_input_list

__all__ = ("run")


def validate_int(
  val: str,
  min_val: Optional[int] = None,
  max_val: Optional[int] = None,
  exp_len: Optional[int] = None
) -> bool:
  try:
    if exp_len is not None:
      assert len(val) == exp_len
    val = int(val)
    if min_val is not None:
      assert val >= min_val
    if max_val is not None:
      assert val <= max_val
  except (ValueError, AssertionError):
    return False
  return True


def validate_hgt(val: str):
  units = {"cm": (150, 193), "in": (59, 76)}
  match = re.fullmatch(r"(\d+)(\w+)", val)

  try:
    min_val, max_val = units[match[2]]
  except (KeyError, TypeError):
    return False
  else:
    return validate_int(match[1], min_val, max_val)


def validate_hcl(val: str) -> bool:
  match = re.fullmatch(r"#[0-9a-f]{6}", val)
  return match is not None


def validate_ecl(val: str) -> bool:
  return val in {
    "amb", "blu", "brn", "gry", "grn", "hzl", "oth"
  }


def validate_pid(val: str) -> bool:
  return validate_int(val, exp_len=9)


class Part(enum.IntEnum):
  A = 1
  B = 2


@dataclasses.dataclass
class Entry:
  byr: str = None
  iyr: str = None
  eyr: str = None
  hgt: str = None
  hcl: str = None
  ecl: str = None
  pid: str = None
  cid: str = None

  VAL_MAP: ClassVar[Mapping[str, Callable]] = {
    "byr": partial(
      validate_int,
      min_val=1920, max_val=2002
    ),
    "iyr": partial(
      validate_int,
      min_val=2010, max_val=2020
    ),
    "eyr": partial(
      validate_int,
      min_val=2020, max_val=2030
    ),
    "hgt": validate_hgt,
    "hcl": validate_hcl,
    "ecl": validate_ecl,
    "pid": validate_pid,
    "cid": lambda _: True
  }

  def is_valid(self, part: Part) -> bool:
    if part is Part.A:
      validate = lambda k, v: v is not None if k != "cid" else True
    elif part is Part.B:
      validate = self.validate_attr
    else:
      raise ValueError("Invalid part.")
    
    return all(
      validate(k, v)
      for k, v in self.__dict__.items()
    )

  def validate_attr(self, attr: str, val: str) -> bool:
    if val is None:
      valid = False if attr != "cid" else True
    else:
      valid = self.VAL_MAP[attr](val)
    return valid

  def update(self, line: str) -> None:
    for item in line.split():
      attr, val = item.split(":")
      setattr(self, attr, val)


def process(lines: List[str], part: Part) -> int:
  i: int = 0
  count: int = 0

  while i < len(lines):
    entry = Entry()
    while i < len(lines) and lines[i]:
      entry.update(lines[i])
      i = i + 1
    if entry.is_valid(part):
      count += 1
    i = i + 1

  return count


#---------------------------------------------------

def run_part_a() -> int: # 200
  return process(get_input_list(4), Part.A)


def run_part_b() -> int: # TODO fix this
  return process(get_input_list(4), Part.B)


def run() -> None:
  print(run_part_a())
  print(run_part_b())


if __name__ == "__main__":
  run()
