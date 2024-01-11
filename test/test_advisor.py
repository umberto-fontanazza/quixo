from src.advisor import Advisor, ALL_ADVISORS, line_majority_count, count_moves
from src.board import PlayerID, random_board
from test.example_boards import board_1, board_2, board_3
from itertools import product

random_boards = [random_board() for _ in range(5)]

def test_advisor_result_type_and_range():
    for advisor, player, board in product(ALL_ADVISORS, [0,1], random_boards):
        p: PlayerID = 'X' if player else 'O'
        score = advisor(board, p)
        assert type(score) in [float, int]
        assert score >= 0
        assert score <= 100

def test_line_majority_count():
    assert line_majority_count(board_1) == (4, 6)
    assert line_majority_count(board_2) == (1, 5)
    assert line_majority_count(board_3) == (6, 2)

def test_count_moves():
    assert count_moves(board_1) == (38, 41)
    assert count_moves(board_2) == (26, 27)
    assert count_moves(board_3) == (29, 31)