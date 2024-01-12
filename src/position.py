from typing import Literal
from itertools import product
from dataclasses import dataclass
from lib.game import Move

@dataclass(frozen=True)
class Position():
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

    @property
    def slides(self) -> list[Move]:
        slides = [slide for slide in Move]
        if self.axis_0 == 0:
            slides.remove(Move.TOP)
        elif self.axis_0 == 4:
            slides.remove(Move.BOTTOM)

        if self.axis_1 == 0:
            slides.remove(Move.LEFT)
        elif self.axis_1 == 4:
            slides.remove(Move.RIGHT)
        return slides

    def as_tuple(self):
        return (self.axis_0, self.axis_1)

CORNERS = [Position(x, y) for x, y in product((0, 4), (0, 4))]
BORDERS = [Position(x, y) for x, y in product((0, 1, 2, 3, 4), (0, 4))] + [Position(x, y) for x, y in product((0, 4), (1, 2, 3))]