from __future__ import annotations
from lib.game import Move
from src.symmetry import Symmetry
from typing import Literal, Iterable
from itertools import product
from dataclasses import dataclass

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

    def symmetric(self, axis: Symmetry) -> Position:
        if axis == Symmetry.HORIZONTAL:
            return Position(4 - self.axis_0, self.axis_1)
        if axis == Symmetry.VERTICAL:
            return Position(self.axis_0, 4 - self.axis_1)
        if axis == Symmetry.DIAGONAL:
            return Position(self.axis_1, self.axis_0)                   # ok, it is the transposed
        if axis == Symmetry.ANTIDIAGONAL:
            return Position(4 - self.axis_1, 4 - self.axis_0)           # ok
        if axis == Symmetry.ROT90:
            return Position(4 - self.axis_1, self.axis_0)               # ok -> np.rot90 rotates counterclockwise
        if axis == Symmetry.ROT180:
            return Position(4 - self.axis_0, 4 - self.axis_1)
        if axis == Symmetry.ROT270:
            return Position(self.axis_1, 4 - self.axis_0)

    def symmetrics(self, axes: Iterable[Symmetry]) -> set[Position]:
        """Returns a set containing self and its symmetrics"""
        return {self.symmetric(axis) for axis in axes} | {self}

    def as_tuple(self):
        return (self.axis_0, self.axis_1)

    # TODO: warning, it's bugged
    @staticmethod
    def filter_out_symmetrics(positions: Iterable[Position], axes: Iterable[Symmetry]) -> set[Position]:
        filtered_positions: set[Position] = set()
        for position in positions:
            symmetrics = position.symmetrics(axes)
            if any(symmetric in filtered_positions for symmetric in symmetrics):
                continue # symmetric already present
            filtered_positions.add(position)
        return filtered_positions

CORNERS: list[Position] = [Position(x, y) for x, y in product((0, 4), (0, 4))]
BORDERS: list[Position] = [Position(x, y) for x, y in product((0, 1, 2, 3, 4), (0, 4))] + [Position(x, y) for x, y in product((0, 4), (1, 2, 3))]