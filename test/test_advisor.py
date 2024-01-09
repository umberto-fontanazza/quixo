from src.advisor import Advisor, ALL_ADVISORS
from src.board import random_board
from itertools import product

def test_advisor_result_type_and_range():
    board = random_board()
    for advisor, player in product(ALL_ADVISORS, [0,1]):
        score = advisor(board, player)
        assert type(score) in [float, int]
        assert score >= 0
        assert score <= 100