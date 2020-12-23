from typing import List
import collections

from .. import utils

__all__ = ("main")

MIN_STEP = 1
MAX_STEP = 3


def count_steps(nums: List[int]):
  counter = collections.defaultdict(int)

  curr = 0
  for num in nums:
    counter[num - curr] += 1
    curr = num
  
  counter[MAX_STEP] += 1 # add built-in adapter

  return counter[MIN_STEP] * counter[MAX_STEP]


def count_combns(nums: List[int]):
  # Memoizing makes a *huge* difference here - since the smallest
  # valid step is always evaluated first, the only path we actually
  # evaluate function calls for is the one with every adapter
  # included - so every subsequent path is entirely made of cache hits!
  # [See phone for a nice diagram.]
  @utils.memoize
  def _count_paths_to_end(start_num: int):
    # Base case: at the end of the list there's only one combination.
    if start_num == nums[-1]:
      return 1
    
    # Return sum all possible paths to the end of the list from here.
    # (C) Debbie Martin - heavily inspired!
    return sum(
      _count_paths_to_end(start_num + step)
      for step in range(MIN_STEP, MAX_STEP + 1)
      if start_num + step in nums
    )

  return _count_paths_to_end(0)


@utils.display
def process(nums: List[int]):
  nums.sort()
  return (
    count_steps(nums), # 3000
    count_combns(nums) # 193434623148032
   )


#---------------------------------------------------

def main() -> None:
  process(utils.get_input_list(__name__, cast_func=int))


if __name__ == "__main__":
  main()
