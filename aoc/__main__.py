import os
import re
import sys
import traceback

from importlib import import_module

def main():
  days = [
    m[:-3] for m in os.listdir("aoc/days")
    if re.fullmatch(r"day\d+\.py", m) is not None
  ]
  for day in sorted(days):
    print(f"### Day {day[3:]}")
    import_module(f".days.{day}", __package__).main()
    print("")


try:
  main()
except Exception as exc:
  traceback.print_exception(*sys.exc_info())
  sys.exit(exc)
