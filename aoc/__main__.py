import os
import re
import sys
import traceback

from importlib import import_module
from typing import List

def run_day(day_mod: str):
  print(f"### Day {day_mod[3:]}")
  import_module(f".days.{day_mod}", __package__).main()
  print("")

def run_all(day_mods: List[str]):
  for day_mod in day_mods:
    run_day(day_mod)

def main():
  day_mods = sorted([
    m[:-3] for m in os.listdir("aoc/days")
    if re.fullmatch(r"day\d+\.py", m) is not None
  ])
  run_day(day_mods[-1])


try:
  main()
except Exception:
  traceback.print_exception(*sys.exc_info())
  sys.exit(1)
