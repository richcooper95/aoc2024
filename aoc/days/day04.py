from typing import List

from .. import utils

__all__ = ("main")


@utils.display
def xmas_search(input_list: List[str]) -> int:
  # Move a 4x4 window across the grid, checking for matches on "XMAS" and "SAMX".
  # Not the most efficient solution, but it's late!
  count = 0
  i = 0
  while i < len(input_list) - 3:
    j = 0
    while j < len(input_list[0]) - 3:
      window = [row[j:j+4] for row in input_list[i:i+4]]
      if get_diag_top_left_to_bottom_right(window) in ["XMAS", "SAMX"]:
        count += 1

      if get_diag_top_right_to_bottom_left(window) in ["XMAS", "SAMX"]:
        count += 1

      if i == 0:
        count += count_words_in_all_rows(window, ["XMAS", "SAMX"])
      elif window[3] in ["XMAS", "SAMX"]:
        count += 1

      if j == 0:
        count += count_words_in_all_columns(window, ["XMAS", "SAMX"])
      elif get_word_in_column(window, 3) in ["XMAS", "SAMX"]:
        count += 1

      j += 1
    i += 1

  return count

@utils.display
def x_mas_search(input_list: List[str]) -> int:
  # Same approach as above, but with a 3x3 window and checking for "MAS" and "SAM" in
  # the diagonals.
  count = 0
  i = 0
  while i < len(input_list) - 2:
    j = 0
    while j < len(input_list[0]) - 2:
      window = [row[j:j+3] for row in input_list[i:i+3]]

      diags = (get_diag_top_left_to_bottom_right(window), get_diag_top_right_to_bottom_left(window))

      if diags in [("MAS", "SAM"), ("SAM", "MAS"), ("MAS", "MAS"), ("SAM", "SAM")]:
        count += 1

      j += 1
    i += 1

  return count

def get_diag_top_left_to_bottom_right(window: List[str]) -> str:
  return "".join(window[i][i] for i in range(len(window)))

def get_diag_top_right_to_bottom_left(window: List[str]) -> str:
  return "".join(window[i][len(window)-i-1] for i in range(len(window)))

def word_in_column(window: List[str], idx: int, word: str) -> bool:
  return all(window[i][idx] == word[i] for i in range(len(word)))

def get_word_in_column(window: List[str], idx: int) -> str:
  return "".join(window[i][idx] for i in range(len(window)))

def count_words_in_all_rows(window: List[str], words: List[str]) -> bool:
  count = 0
  for row in window:
    if row in words:
      count += 1

  return count

def count_words_in_all_columns(window: List[str], words: List[str]) -> bool:
  count = 0
  for i in range(len(window)):
    if get_word_in_column(window, i) in words:
      count += 1

  return count


#---------------------------------------------------

def main() -> None:
  input_list = utils.get_input_list(__name__)
  xmas_search(input_list)
  x_mas_search(input_list)


if __name__ == "__main__":
  main()
