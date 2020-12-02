from typing import List

from ..utils import get_input

__all__ = ("run")


class PairNotFoundError(Exception):
  pass

class TripletNotFoundError(Exception):
  pass


def find_pair_product(
  nums: List[int],
  total: int
) -> int:
  nums.sort()
  i = 0
  j = len(nums) - 1
  while i < j:
    if nums[i] + nums[j] == total:
      return nums[i] * nums[j]
    if nums[i] + nums[j] < total:
      i += 1
    elif nums[i] + nums[j] > total:
      j -= 1
  raise PairNotFoundError


def find_triplet_product(nums) -> int:
  for n in nums:
    try:
      return n * find_pair_product(nums, 2020 - n)
    except PairNotFoundError:
      pass
  raise TripletNotFoundError

#--------------------------------------------------------------

def run_part_a() -> int: # 73371
  # Find product of pair which sums to 2020
  return find_pair_product(get_input(1, cast_func=int), 2020)


def run_part_b() -> int: # 127642310
  # Find product of triplet which sums to 2020
  return find_triplet_product(get_input(1, cast_func=int))


def run() -> None:
  print(run_part_a())
  print(run_part_b())


if __name__ == "__main__":
  run()
