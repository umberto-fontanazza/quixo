from typing import Literal
from dataclasses import dataclass
from itertools import product

@dataclass(frozen=True)
class Position(tuple):
    axis_0: Literal[0, 1, 2, 3, 4]
    axis_1: Literal[0, 1, 2, 3, 4]

    def __getitem__(self, index: int):
        if index == 0:
            return self.axis_0
        if index == 1:
            return self.axis_1
        raise ValueError(f'{index =} not valid. Must be 0 or 1')

    def is_border(self) -> bool:
        if self.axis_0 in (0, 4):
            return True
        if self.axis_1 in (0, 4):
            return True
        return False

    def is_corner(self) -> bool:
        if self.axis_0 not in (0, 4):
         return False
        if self.axis_1 not in (0, 4):
            return False
        return True

# TODO: check this
# before: CORNERS = [Position(x, y) for x, y in product((0, 4), (0, 4))]
CORNERS = [Position(axis_0=x, axis_1=y) for x, y in product((0, 4), (0, 4))]
BORDERS = [Position(axis_0=x, axis_1=y) for x, y in product((0, 1, 2, 3, 4), (0, 4))] + [Position(axis_0=x, axis_1=y) for x, y in product((0, 4), (1, 2, 3))]