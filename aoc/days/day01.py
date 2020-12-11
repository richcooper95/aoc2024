from typing import List

from .. import utils

__all__ = ("main")


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

def main() -> None:
  nums = utils.get_input_list(__name__, cast_func=int)
  print(find_pair_product(nums, 2020)) # 73371
  print(find_triplet_product(nums)) # 127642310


if __name__ == "__main__":
  main()
