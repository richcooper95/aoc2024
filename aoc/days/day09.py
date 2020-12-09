from typing import List
import collections
import itertools

from ..utils import get_input_list

__all__ = ("run")

PREAMBLE = 25

def get_invalid_num(nums: List[int]) -> int:
  curr = PREAMBLE
  preceding_nums = collections.deque(itertools.islice(nums, PREAMBLE))

  for num in itertools.islice(nums, PREAMBLE, None):
    s = set(nums)
    valid = False

    for preceding_num in preceding_nums:
      if num - preceding_num in s:
        valid = True
        break

    if not valid:
      return num
    else:
      preceding_nums.append(num)
      curr += 1
      preceding_nums.popleft()
  
  raise ValueError("No invalid number present in input.")


def get_weakness(invalid_num: int, nums: List[int]) -> int:
  candidate_slice = collections.deque()
  total = 0

  for num in nums:
    candidate_slice.append(num)
    total += num
  
    while total > invalid_num:
      total -= candidate_slice.popleft()
  
    if total == invalid_num:
      return min(candidate_slice) + max(candidate_slice)
  
  raise ValueError("No weakness present in input.")
  

#---------------------------------------------------

def run() -> None:
  nums = get_input_list(9, cast_func=int)
  invalid_num = get_invalid_num(nums)
  weakness = get_weakness(invalid_num, nums)
  print(invalid_num) # 552655238
  print(weakness) # 70672245


if __name__ == "__main__":
  run()
