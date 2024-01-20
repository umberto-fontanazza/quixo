from src.board import Board, CompleteMove
from src.player import PlayerID
from lib.game import Move
from src.position import CORNERS, CENTER
import numpy as np

# TODO: define some stats for the board: when you put one in, add both cases (new board, from parent board)

class BoardStats:
    def __init__(self,  board: Board, parent_board: Board | None = None, move: CompleteMove | None = None, player: PlayerID | None = None) -> None:
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


    @property
    def all_stats(self) -> list:
        """get all the stats of the board"""
        return [
            self.x_count,
            self.o_count,
            self.x_available_moves,
            self.o_available_moves,
            self.x_corner_control,
            self.o_corner_control,
            self.x_center_control,
            self.o_center_control,
            self.empty_spaces
        ]