from typing import Dict, List
import dataclasses
import math

from .. import utils

__all__ = ("main")


@dataclasses.dataclass
class Schedule:
  buses: Dict[int, str]

  def get_service_info_after(self, start_time: int):
    t = start_time
  
    while True:
      for bus_id in self.buses.values():
        if not t % int(bus_id):
          return int(bus_id), t - start_time
      t += 1
  

  # (C) Martin Henstridge - significantly speedier than my solution!
  def find_timestamp_consecutive_services(self):
    """
    Find a time t s.t. all idx, bus_id pairs satisfy (t + idx) % bus_id == 0.

    Instead of incrementing through all times and checking they satisfy the
    equation for all buses (my original very slow solution), we increment
    through all *buses* and on each iteration find the lowest t which is the
    solution for all buses so far (starting from the t which was a solution
    for all previous buses) by an increment which is the LCM of all previous
    Bus IDs (because this guarantees that any t we try for the current bus is
    also a solution for all previous buses).

    NB: We use the fact that all Bus IDs are prime to just multiply them
        together for the LCM calculation.

    Increasing the increment like this means we converge on the correct t
    *significantly* faster - the increment grows rapidly:
  
    idx 0, bus_id 13:  13
    idx 7, bus_id 37:  481
    idx 13, bus_id 401:  192881
    idx 27, bus_id 17:  3278977
    idx 32, bus_id 19:  62300563
    idx 36, bus_id 23:  1432912949
    idx 42, bus_id 29:  41554475521
    idx 44, bus_id 613:  25472893494373
    """
    t = 0
    increment = 1

    for idx, bus_id in self.buses.items():
      while (t + idx) % bus_id:
        t += increment
      increment *= bus_id
  
    return t


@utils.display
def process(input_list: List[str]):
  try:
    start = int(input_list[0])
    intervals = {
      idx: int(t)
      for idx, t in enumerate(input_list[1].split(","))
      if t != "x"
    }
  except ValueError as exc:
    raise ValueError(f"Invalid input: {exc}") from exc

  schedule = Schedule(intervals)

  return (
    math.prod(schedule.get_service_info_after(start)), # 136
    schedule.find_timestamp_consecutive_services() # 305068317272992
  )


#---------------------------------------------------

def main() -> None:
  process(utils.get_input_list(__name__))


if __name__ == "__main__":
  main()
