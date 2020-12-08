from typing import List, Tuple
from collections import defaultdict

from ..utils import get_input_list

__all__ = ("run")


def process(lines: List[str]) -> Tuple[int]:
  capacity_map = dict() # map a bag to the bags it can contain
  container_map = defaultdict(set) # map a bag to the bags which can contain it

  for line in lines:
    # TODO: improve error handling of badly-formatted entries here
    bag, bag_info = line.split(" bags contain ")
    if "no other" in bag_info:
      # set value to empty list to allow common treatment during later walk
      capacity_map[bag] = []
    else:
      # set the value to a list of tuples containing the count and bag type for
      # all bags it can contain
      capacity_map[bag] = [
        (int(elem[0]), elem[2:elem.index(" bag")])
        for elem in bag_info.split(", ")
      ]
      # add the bag to all the contained bags in the container map
      for b in capacity_map[bag]:
        container_map[b[1]].add(bag)
  
  def _walk_containers(_bag: str):
    containers = set()
    for container in container_map[_bag]:
      containers.add(container)
      containers.update(_walk_containers(container))
    return containers

  def _walk_contained(_bag: str):
    num_bags = 0
    for inner_bag in capacity_map[_bag]:
      num_bags += inner_bag[0]*(1 + _walk_contained(inner_bag[1]))
    return num_bags

  return len(_walk_containers("shiny gold")), _walk_contained("shiny gold")
  

#---------------------------------------------------

def run() -> None:
  res_a, res_b = process(get_input_list(7))
  print(res_a) # 213
  print(res_b) # 38426


if __name__ == "__main__":
  run()
