from typing import List

from ..utils import get_input_list

__all__ = ("run")


class PairNotFoundError(Exception):
  pass

class TripletNotFoundError(Exception):
  pass


# O(N)
def find_pair_product(
  nums: List[int],
  total: int
) -> int:
  s = set(nums)
  for num in nums:
    complement = total - num
    if complement in s:
      return num * complement
  raise PairNotFoundError


# O(N^2)
def find_triplet_product(nums) -> int:
  for n in nums:
    try:
      return n * find_pair_product(nums, 2020 - n)
    except PairNotFoundError:
      pass
  raise TripletNotFoundError

#---------------------------------------------------

def run_part_a() -> int: # 73371
  # Find product of pair which sums to 2020
  return find_pair_product(get_input_list(1, cast_func=int), 2020)


def run_part_b() -> int: # 127642310
  # Find product of triplet which sums to 2020
  return find_triplet_product(get_input_list(1, cast_func=int))


def run() -> None:
  print(run_part_a())
  print(run_part_b())


if __name__ == "__main__":
  run()
