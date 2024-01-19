from __future__ import annotations
from lib.game import Move
from src.position import Position, BORDERS
from src.symmetry import Symmetry
from src.player import PlayerID, player_int, change_player
from typing import Literal, Annotated
from numpy.typing import NDArray
from copy import deepcopy
from functools import lru_cache
from src.board_stats import BoardStats
import numpy as np

Outcome = Literal['Win', 'Loss']
CompleteMove = tuple[Position, Move]

class Board():
    def __init__(self, array: Annotated[NDArray[np.int8], Literal[5, 5]] | None = None):
        self.__board = array if array is not None else np.full((5, 5), -1, dtype=np.int8)
        self.__stats: BoardStats | None = None

    @property
    def stats(self, parent_board = None, move = None, player = None) -> BoardStats:
        """get the stats of the board, can also be computed """
        if self.__stats is None:
            self.__stats = BoardStats(self, parent_board, move)
        return self.__stats

    @property
    def ndarray(self) -> NDArray[np.int8]:
        return deepcopy(self.__board)

    @property
    @lru_cache(maxsize = 2048)
    def symmetries(self) -> set[Symmetry]:
        matrix = self.__board
        _symmetries: set[Symmetry] = set()
        if np.array_equal(matrix, np.flipud(matrix)):
            _symmetries.add(Symmetry.HORIZONTAL)
        if np.array_equal(matrix, np.fliplr(matrix)):
            _symmetries.add(Symmetry.VERTICAL)
        if np.array_equal(matrix, matrix.T):
            _symmetries.add(Symmetry.DIAGONAL)
        if np.array_equal(matrix, np.rot90(np.rot90(matrix).T, -1)):
            _symmetries.add(Symmetry.ANTIDIAGONAL)
        if np.array_equal(matrix, np.rot90(matrix, k=1)):
            _symmetries.add(Symmetry.ROT90)
        if np.array_equal(matrix, np.rot90(matrix, k=2)):
            _symmetries.add(Symmetry.ROT180)
        if np.array_equal(matrix, np.rot90(matrix, k=3)):
            _symmetries.add(Symmetry.ROT270)
        return _symmetries

    @staticmethod
    def random() -> Board:
        arr = np.random.choice([0, 1, -1], size=(5,5)).astype(np.int8)
        return Board(arr)

    @staticmethod
    def change_symbols(board: NDArray) -> NDArray:
        """Takes in a board where   empty = -1, O =  0 and X = 1 and
        returns a board where       empty =  0, O = -1 and X = 1"""
        b: NDArray = deepcopy(board)
        b = b * 2
        b = b -1
        b[b == -3] = 0
        return b

    @lru_cache(maxsize = 2048)
    def list_moves(self, current_player: Literal[0, 1, 'O', 'X'], shuffle = True, filter_out_symmetrics = False) -> list[tuple[Position, Move]]:
        """returns all the possible moves given a Game object
            that is, a list of tuples (Position, Move)"""
        current_player = 0 if current_player == 0 or current_player == 'O' else 1
        legal_moves = []
        board = self.__board
        available_cells = {cell for cell in BORDERS if board[cell] == -1 or board[cell] == current_player}
        explorable_position = available_cells if not filter_out_symmetrics else Position.filter_out_symmetrics(available_cells, self.symmetries)
        for position in explorable_position:
            slides: list[Move] = position.slides
            pos_and_slides = [(position, slide) for slide in slides]
            legal_moves += pos_and_slides
        if shuffle:
            np.random.shuffle(legal_moves)
        return legal_moves

    def count_moves(self) -> tuple[int, int]:
        """Returns the count of all available moves for O and for X as a tuple.
        A piece taken from the corner of the board accounts for 2 moves while a piece
        from the side accounts for 3 moves."""
        o_moves_count, x_moves_count = 0, 0
        for position in BORDERS:
            slide_count = 2 if position.is_corner() else 3
            if self.__board[position] == -1:
                o_moves_count += slide_count
                x_moves_count += slide_count
            elif self.__board[position] == 1:
                x_moves_count += slide_count
            else:
                o_moves_count += slide_count
        return (o_moves_count, x_moves_count)

    @lru_cache(maxsize = 2048)
    def check_winners(self) -> set[PlayerID]:
        '''Check the winner.
        Returns the player IDs that have a winning row, column, or diagonal'''
        _winners: set[PlayerID] = set()
        for line in self.lines:
            if (line == line[0]).all():
                if line[0] == -1:
                    continue
                _winners.add(line[0])
                if len(_winners) == 2:
                    break
        return _winners

    @property
    def game_over(self) -> bool:
        return len(self.check_winners()) != 0

    @lru_cache(maxsize = 2048)
    def winner(self, *, current_player: PlayerID) -> Literal[0, 1] | None:
        """The opponent of @param{current_player} made the move which produced this board"""
        current_player = player_int(current_player)
        opponent = change_player(current_player)
        winners = self.check_winners()
        if current_player in winners:
            return current_player
        elif opponent in winners:
            return opponent
        return None

    @lru_cache(maxsize=2048)
    def move(self, move: tuple[Position, Move], current_player: Literal[0, 1, 'X', 'O']) -> Board:
        """applies move to the board - out of place"""
        current_player = 1 if current_player == 1 or current_player == 'X' else 0
        arr = self.ndarray
        position, _ = move
        arr[position] = current_player
        return Board(self.__slide(arr, move))

    @staticmethod
    def __slide(board: NDArray, move: tuple[Position, Move]) -> NDArray:
        position, slide = move
        axis_0, axis_1 = position
        if slide == Move.RIGHT:
            board[axis_0, axis_1:] = np.roll(board[axis_0, axis_1:], -1)
        elif slide == Move.LEFT:
            board[axis_0, :(axis_1+1)] = np.roll(board[axis_0, :(axis_1+1)], 1)
        elif slide == Move.BOTTOM:
            board[axis_0:, axis_1] = np.roll(board[axis_0:, axis_1], -1)
        elif slide == Move.TOP:
            board[:(axis_0+1), axis_1] = np.roll(board[:(axis_0+1), axis_1], 1)
        return board

    @property
    def lines(self) -> list[NDArray[np.int8]]:
        """Returns a list of 12 ndarrays, one for each row, col and diag"""
        arr = self.ndarray
        _lines: list[NDArray] = [row for row in arr]
        _lines += [col for col in np.transpose(arr)]
        _lines += [arr.diagonal()]
        _lines += [arr[::-1].diagonal()]
        return _lines

    @property
    def is_empty(self):
        return np.array_equal(self.ndarray, Board().ndarray)

    def check_for_terminal_conditions(self, current_player: PlayerID) -> int:
        """given a terminal state board, return a valid minmax value
            if no one won, returns -1"""
        winners: set[PlayerID] = self.check_winners()
        opponent = 0 if current_player in (1, 'X') else 1
        if opponent in winners:
            return 0
        if current_player in winners:
            return 100
        return -1

    @property
    def min_played_moves(self) -> int:
        return (self.ndarray != Board().ndarray).sum()