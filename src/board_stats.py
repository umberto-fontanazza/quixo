from __future__ import annotations
from lib.game import Move
from src.board import Board, CompleteMove
from src.position import Position, CORNERS
from typing import Annotated, Literal
from numpy.typing import NDArray
import numpy as np

class BoardStats(Board):
    def __init__(self,
                 available_moves = (44, 44, 44),
                 center_control = (0, 0, 9),
                 array: Annotated[NDArray[np.int8], Literal[5, 5]] | None = None):
        super().__init__(array)
        # super().__init__.__args qualcosa... per non riscrivere gli argomenti, da vedere
        self.available_moves = available_moves
        self.center_control = center_control

        o, x = 0, 0
        for corner in CORNERS:
            if self[corner] == 0:
                o += 1
            elif self[corner] == 1:
                x += 1
        self.corner_control = (o, x, 4)

    """     def __init__(self,  board: Board, parent_board: Board | None = None, move: CompleteMove | None = None, player: PlayerID | None = None) -> None:
        # define stats that have to computed from scratch every time
        n_available_moves = board.count_moves()
        # TODO: add more of these
        self.x_available_moves = n_available_moves[1]
        self.o_available_moves = n_available_moves[0]
        self.x_corner_control = np.sum(board.ndarray[list(CORNERS)] == 1)
        self.o_corner_control = np.sum(board.ndarray[list(CORNERS)] == 0)
        self.x_center_control = np.sum(board.ndarray[list(CENTER)] == 1)
        self.o_center_control = np.sum(board.ndarray[list(CENTER)] == 0)

        # define how to compute stats from a parent board (all the info at your disposal)
        if parent_board is not None and move is not None and player is not None:
            arr_parent = parent_board.ndarray
            if arr_parent[move[0]] == -1:
                if player in ('X', 1):
                    self.x_count = parent_board.stats.x_count + 1
                else:
                    self.o_count = parent_board.stats.o_count + 1
                self.empty_spaces = parent_board.stats.empty_spaces - 1
            else:
                self.o_count, self.x_count = parent_board.stats.o_count, parent_board.stats.x_count
                self.empty_spaces = parent_board.stats.empty_spaces

        # define how to compute the SAME stats on a new board
        else:
            arr_board = board.ndarray
            self.x_count = np.sum(arr_board[arr_board == 1])
            self.o_count = np.sum(arr_board[arr_board == 0])
            self.empty_spaces = np.sum(arr_board[arr_board == -1])
     """

    def move(self, move: CompleteMove, current_player: Literal[0, 1, 'X', 'O']) -> BoardStats:
        next_board: Board = super().move(move, current_player)
        position, slide = move
        # either board[pos[0][:]] board[[:][pos[0]]]
        vertical = slide == Move.BOTTOM or slide == Move.TOP
        array: NDArray = self.ndarray
        sliding_line = array[:, position[1]] if vertical else array[position[0], :]

        # available moves recalc
        line_score = [0, 0, 13]
        for index in range(5):
            if sliding_line[index] == -1:
                continue
            player_index = sliding_line[index]
            line_score[player_index] += 2 if index in (0, 4) else 3

        o_am, x_am, neutral_am = self.available_moves
        if current_player in ('X', 1) and self[position] == -1:
            o_am -= 1
        return BoardStats(available_moves = (o_am , x_am, neutral_am), array = next_board.ndarray)

    # @property
    # def all_stats(self) -> list:
    #     """get all the stats of the board"""
    #     return [
    #         self.x_count,
    #         self.o_count,
    #         self.x_available_moves,
    #         self.o_available_moves,
    #         self.x_corner_control,
    #         self.o_corner_control,
    #         self.x_center_control,
    #         self.o_center_control,
    #         self.empty_spaces
    #     ]