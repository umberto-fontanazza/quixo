from src.oracle import Oracle
from src.board import random_board

test_boards = [random_board() for _ in range(10)]

def test_oracle_advantage_type_and_range():
    o = Oracle()
    player = 'X'
    for board in test_boards:
        score = o.advantage(board, player)
        assert type(score) in [int, float]
        assert score >= 0
        assert score <= 100
