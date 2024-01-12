from src.advisor import Advisor, ALL_ADVISORS, line_majority_count
from src.board import PlayerID, Board
from test.example_boards import board_1, board_2, board_3, example_boards
from itertools import product

def test_advisor_result_type_and_range():
    for advisor, player, board in product(ALL_ADVISORS, [0,1], example_boards):
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
    assert board_1.count_moves() == (38, 41)
    assert board_2.count_moves() == (26, 27)
    assert board_3.count_moves() == (29, 31)