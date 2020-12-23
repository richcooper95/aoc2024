from typing import List

from .. import utils

__all__ = ("main")


@utils.display
def process(input_list: List[str], part: utils.Part):
  nums = input_list[0].split(",")

  # Place all numbers apart from the last into the history.
  # This maps each number to the turn it was last spoken.
  history = {
    int(num): idx + 1
    for idx, num in enumerate(nums[:-1])
  }

  max_idx = 2020 if part is utils.Part.A else 30000000

  # Stage the most recently spoken so we can use it to determine
  # the next number, before adding it to the history.
  prev = int(nums[-1])
  prev_idx = len(nums)

  # Play the game!
  while prev_idx < max_idx:
    new = prev_idx - history[prev] if prev in history else 0
    history[prev] = prev_idx
    prev_idx += 1
    prev = new

  return prev


#---------------------------------------------------

def main() -> None:
  input_list = utils.get_input_list(__name__)
  process(input_list, utils.Part.A) # 1696
  process(input_list, utils.Part.B) # 37385


if __name__ == "__main__":
  main()
