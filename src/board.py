from __future__ import annotations
from lib.game import Move
from src.position import Position, BORDERS
from typing import Literal, Annotated
from copy import deepcopy
from numpy.typing import NDArray
from src.symmetry import Symmetry
import numpy as np


PlayerID = Literal['X', 'O', 1, 0]
Outcome = Literal['Win', 'Loss']

class Board():
    def __init__(self, array: Annotated[NDArray[np.int8], Literal[5, 5]] | None = None):
        self.__board = array if array is not None else np.full((5, 5), -1, dtype=np.int8)

    @property
    def ndarray(self) -> NDArray[np.int8]:
        return deepcopy(self.__board)

    @property
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

    def list_moves(self, current_player: Literal[0, 1, 'O', 'X'], shuffle = True, filter_out_symmetrics = False) -> list[tuple[Position, Move]]:
        """returns all the possible moves given a Game object
            that is, a list of tuples (Position, Move)"""
        current_player = 0 if current_player == 0 or current_player == 'O' else 1
        legal_moves = []
        board = self.__board
        symmetry_axes = self.symmetries if filter_out_symmetrics else set()
        explorable_position = Position.filter_out_symmetrics(BORDERS, symmetry_axes)
        for position in explorable_position:
            if board[position.as_tuple()] != -1 and board[position.as_tuple()] != current_player:
                continue # it belongs to the opponent, ignore
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
            if self.__board[position.as_tuple()] == -1:
                o_moves_count += slide_count
                x_moves_count += slide_count
            elif self.__board[position.as_tuple()] == 1:
                x_moves_count += slide_count
            else:
                o_moves_count += slide_count
        return (o_moves_count, x_moves_count)

    def check_winners(self) -> set[PlayerID]:
        '''Check the winner.
        Returns the player IDs that have a winning row, column, or diagonal'''
        _winners: set[PlayerID] = set()
        for line in self.lines:
            if (line == line[0]).all():
                if line[0] == -1:
                    continue
                _winners.add(line[0])
        return _winners

    def move(self, move: tuple[Position, Move], current_player: Literal[0, 1, 'X', 'O']) -> Board:
        """applies move to the board - out of place"""
        current_player = 1 if current_player == 1 or current_player == 'X' else 0
        arr = self.ndarray
        position, _ = move
        assert type(position) == Position
        arr[position.as_tuple()] = current_player
        return Board(self.__slide(arr, move))

    @staticmethod
    def __slide(board: NDArray, move: tuple[Position, Move]) -> NDArray:
        position, slide = move
        axis_0, axis_1 = position.as_tuple()
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

    @staticmethod
    def check_for_terminal_conditions(board: Board, current_player: Literal[0,1] ) -> int:
        """given a terminal state board, return a valid minmax value
            if no one won, returns -1"""
        winners = board.check_winners()
        opponent = 0 if current_player == 1 else 1
        if opponent in winners:
            return 0
        if current_player in winners:
            return 100
        return -1
