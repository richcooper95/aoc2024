from importlib import import_module
import datetime

def run():
  for day in range(1, datetime.datetime.today().day + 1):
    print(f"### Day {day:02d}")
    import_module(f".days.day{day:02d}", __package__).run()
    print("")
