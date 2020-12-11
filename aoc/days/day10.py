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
  # memoizing makes a *huge* difference here - since the smallest
  # valid step is always evaluated first, the only path we actually
  # evaluate function calls for is the one with every adapter
  # included - so every subsequent path is entirely made of cache hits!
  # [see phone for a nice diagram]
  @utils.memoize
  def _count_paths_to_end(start_num: int):
    # base case: at the end of the list there's only one combination
    if start_num == nums[-1]:
      return 1
    
    # return sum all possible paths to the end of the list from here
    # (C) Debbie Martin - heavily inspired!
    return sum(
      _count_paths_to_end(start_num + step)
      for step in range(MIN_STEP, MAX_STEP + 1)
      if start_num + step in nums
    )

  return _count_paths_to_end(0)


#---------------------------------------------------

def main() -> None:
  sorted_nums = sorted(utils.get_input_list(__name__, cast_func=int))
  res_a = count_steps(sorted_nums)
  res_b = count_combns(sorted_nums)
  print(res_a) # 3000
  print(res_b) # 193434623148032


if __name__ == "__main__":
  main()
