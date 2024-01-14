from lib.game import Move
from src.board import Board
from src.position import Position
from src.symmetry import Symmetry
from test.example_boards import board_1, board_2, board_3, example_boards
from itertools import product
from numpy import all, array
from numpy.typing import NDArray

def test_list_moves_return_type():
    moves = board_2.list_moves('X')
    first_move = moves[0]
    position, slide = first_move
    assert type(moves) == list
    assert type(first_move) == tuple
    assert type(position) == Position
    assert type(slide) == Move

def test_list_moves():
    moves = set(board_1.list_moves(1)) # 1 means X
    assert (Position(0, 0), Move.RIGHT) in moves
    assert (Position(4, 3), Move.TOP) not in moves
    assert (Position(4, 1), Move.BOTTOM) not in moves

def test_list_moves2():
    # random tests
    for board in example_boards:
        O_moves, X_moves = board.list_moves('O'), board.list_moves('X')
        assert len(O_moves) + len(X_moves) > 0
    # test board with no valid moves
    board = Board(array([1] * 25).reshape(5, 5))
    assert len(board.list_moves("O")) == 0
    # test number of valid moves
    assert len(board.list_moves("X")) == (12 * 3 + 4 * 2)
    # test should give only 2 valid moves
    arr = board.ndarray
    arr[0, 0] = 0
    edited_board = Board(arr)
    assert len(edited_board.list_moves("O")) == 2

def test_list_moves_3():
    board = Board(array([[ 1,  1, -1,  0,  0],
                         [ 0, -1, -1, -1,  0],
                         [ 0, -1, -1, -1,  0],
                         [ 1,  0, -1, -1, -1],
                         [ 1,  1,  1,  0, -1]]))
    assert len(board.list_moves(1)) == 24

def test_apply_move():
    move = Position(0, 3), Move.LEFT
    actual_result = board_1.move(move, 'X').ndarray
    expected_result = array([
        [ 1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, -1,  0, -1],
        [-1,  1,  1,  0,  1],
        [-1, -1, -1,  0, -1]])
    assert (actual_result == expected_result).all()


def test_lines():
    actual = board_1.lines
    expected = [
        array([-1, -1, -1, 1, -1]),
        array([-1, -1, -1, -1, -1]),
        array([-1, -1, -1, 0, -1]),
        array([-1, 1, 1, 0, 1]),
        array([-1, -1, -1, 0, -1]),
        array([-1, -1, -1, -1, -1]),
        array([-1, -1, -1, 1, -1]),
        array([-1, -1, -1, 1, -1]),
        array([1, -1, 0, 0, 0]),
        array([-1, -1, -1, 1, -1]),
        array([-1, -1, -1, 0, -1]),
        array([-1, 1, -1, -1, -1]),
    ]

    for actual_line, expected_line in zip(actual, expected):
        assert (actual_line == expected_line).all()

def test_symmetries():
    assert board_1.symmetries == set()
    assert board_2.symmetries == set()
    assert board_3.symmetries == set()
    assert Board().symmetries == {s for s in Symmetry}

def test_min_played_moves():
    assert board_1.min_played_moves == 7