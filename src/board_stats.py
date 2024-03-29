from __future__ import annotations
from lib.game import Move
from src.board import Board, CompleteMove
from src.position import Position, CORNERS, BORDERS, CENTER, ALL_POSITIONS
from typing import Annotated, Literal
from numpy.typing import NDArray
import numpy as np

class BoardStats(Board):
    def __init__(self,
                 available_moves = (44, 44, 44),
                 center_control = (0, 0, 9),
                 count_pieces = (0, 0, 25),
                 array: Annotated[NDArray[np.int8], Literal[5, 5]] | None = None,
                 recompute: bool = True):
        super().__init__(array)
        # TODO: super().__init__.__args qualcosa... per non riscrivere gli argomenti, da vedere
        self.available_moves = available_moves
        self.center_control = center_control
        self.count_pieces = count_pieces

        # need to be computed anyway / not worth to use previous stats
        o, x = 0, 0
        for corner in CORNERS:
            if self[corner] == 0:
                o += 1
            elif self[corner] == 1:
                x += 1
        self.corner_control = (o, x, 4)

        # if the parent board / move is unknown, recompute
        if recompute:
            self.__recompute_all_stats()


    # TODO: test
    def __recompute_all_stats(self) -> None:
        """compute the stats from scratch but the ones computed by __init__"""
        array = self.ndarray
        # compute available moves
        o_am, x_am = 0, 0
        for position in BORDERS:
            available_moves = 2 if position in CORNERS else 3
            if array[position] in (0, -1):
                o_am += available_moves
            if array[position] in (1, -1):
                x_am += available_moves
        self.available_moves = (o_am, x_am, 44)

        # compute center control
        o_cc, x_cc = 0, 0
        for position in CENTER:
            if array[position] == 0:
                o_cc += 1
            elif array[position] == 1:
                x_cc += 1
        self.center_control = (o_cc, x_cc, 9)

        # compute pieces count
        o_cp, x_cp = 0, 0
        for position in ALL_POSITIONS:
            if array[position] == 0:
                o_cp += 1
            elif array[position] == 1:
                x_cp += 1
        self.count_pieces = (o_cp, x_cp, 25)


    def move(self, move: CompleteMove, current_player: Literal[0, 1, 'X', 'O']) -> BoardStats:
        next_board: Board = super().move(move, current_player)
        position, slide = move
        vertical = slide == Move.BOTTOM or slide == Move.TOP
        parent_array: NDArray = self.ndarray
        next_array: NDArray = next_board.ndarray
        parent_sliding_line = parent_array[:, position[1]] if vertical else parent_array[position[0], :]
        new_sliding_line = next_array[:, position[1]] if vertical else next_array[position[0], :]
        slide_on_border = (vertical and position[1] in (0,4)) or (not vertical and position[0] in (0,4))
        player_idx = 1 if current_player in ('X',1) else 0
        opponent = 1 - player_idx

        # recompute available_moves
        o_am, x_am, neutral_am = self.available_moves
        parent_line_am, new_line_am = ([0]*3, [0]*3)            # [count_o, count_x, count_neut]
        for i in range(5):
            if slide_on_border:
                avail_moves_for_case = 2 if i in (0,4) else 3
            else:
                avail_moves_for_case = 3 if i in (0,4) else 0
            parent_line_am[parent_sliding_line[i]] += avail_moves_for_case
            new_line_am[new_sliding_line[i]] += avail_moves_for_case
        for i in (0,1):                                         # add 'neutral' to x and o
            parent_line_am[i] += parent_line_am[-1]
            new_line_am[i] += new_line_am[-1]
        o_am += new_line_am[0] - parent_line_am[0]
        x_am += new_line_am[1] - parent_line_am[1]

        # recompute center_control
        o_cc, x_cc, neutral_cc = self.center_control
        if not slide_on_border:                                 # slide on border -> no change to board centre
            parent_line_cc, new_line_cc = ([0]*3, [0]*3)        # [count_o, count_x, count_neut]
            for i in range(1,4):
                parent_line_cc[parent_sliding_line[i]] += 1
                new_line_cc[new_sliding_line[i]] += 1
            for i in (0,1):                                     # add 'neutral' to x and o
                parent_line_cc[i] += parent_line_cc[0]
                new_line_cc[i] += new_line_cc[0]
            o_cc += new_line_cc[0] - parent_line_cc[0]
            x_cc += new_line_cc[1] - parent_line_cc[1]

        # recompute count_pieces
        o_cp, x_cp, neutral_cp = self.count_pieces
        if parent_array[position] == -1:                        # if player did not take a blank piece -> skip
            o_cp += (1 if player_idx == 0 else 0)
            x_cp += (1 if player_idx == 1 else 0)

        return BoardStats(available_moves = (o_am , x_am, neutral_am),
                            center_control = (o_cc, x_cc, neutral_cc),
                            count_pieces = (o_cp, x_cp, neutral_cp),
                            array = next_array,
                            recompute = False)



    @property
    def all_stats(self) -> list[tuple[int, int, int]]:
        """get all the stats of the board:
        corner_control,
        available_moves,
        center_control,
        count_pieces
        """
        return [
            self.corner_control,
            self.available_moves,
            self.center_control,
            self.count_pieces
        ]