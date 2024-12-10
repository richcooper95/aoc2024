import dataclasses

from typing import List

from .. import utils

__all__ = ("main")


@dataclasses.dataclass
class Equation:
  value: int
  operands: List[int]

  @classmethod
  def from_line(cls, line: str) -> "Equation":
    value, operands = line.split(": ")
    return cls(int(value), list(map(int, operands.split())))

  def solvable(self) -> int:
    # Return the value if the equation is solvable, otherwise return 0.
    # Try every possible combination of operators.
    def _solve(operands: List[int]) -> int:
      if len(operands) == 2:
        if operands[0] + operands[1] == self.value:
          return self.value

        if operands[0] * operands[1] == self.value:
          return self.value

        if int(str(operands[0]) + str(operands[1])) == self.value:
          return self.value

        return 0

      # (C) Derik - nice easy optimisation!
      if operands[0] > self.value:
        return 0

      with_plus = _solve([operands[0] + operands[1]] + operands[2:])
      if with_plus == self.value:
        return self.value

      with_multiply = _solve([operands[0] * operands[1]] + operands[2:])
      if with_multiply == self.value:
        return self.value

      with_concatenation = _solve([int(str(operands[0]) + str(operands[1]))] + operands[2:])
      if with_concatenation == self.value:
        return self.value

      return 0

    return _solve(self.operands)


@utils.display
def true_equations(equations: List[Equation]) -> int:
  total = 0
  for equation in equations:
    total += equation.solvable()

  return total


#---------------------------------------------------

def main() -> None:
  equations = utils.get_input_list(__name__, cast_func=Equation.from_line)
  true_equations(equations)


if __name__ == "__main__":
  main()
