from src.board import get_possible_moves
from lib.game import Move
from test.example_boards import board_1, board_2, board_3

def test_get_possible_moves():
    moves = set(get_possible_moves(board_1, 1)) # 1 means current player is X
    assert ((0, 0), Move.RIGHT) in moves