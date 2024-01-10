from src.advisor import Advisor, ALL_ADVISORS, line_majority_count
from src.board import Player, random_board
from itertools import product
from numpy import array

board_1 = array([   [-1, -1, -1,  1, -1],
                    [-1, -1, -1, -1, -1],
                    [-1, -1, -1,  0, -1],
                    [-1,  1,  1,  0,  1],
                    [-1, -1, -1,  0, -1]])

random_boards = [random_board() for _ in range(5)]

def test_advisor_result_type_and_range():
    for advisor, player, board in product(ALL_ADVISORS, [0,1], random_boards):
        p: Player = 'X' if player else 'O'
        score = advisor(board, p)
        assert type(score) in [float, int]
        assert score >= 0
        assert score <= 100

def test_line_majority_count():
    assert line_majority_count(board_1) == (4, 6)