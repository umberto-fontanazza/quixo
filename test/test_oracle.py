from src.oracle import Oracle
from src.board import Board
from test.example_boards import example_boards

def test_oracle_advantage_type_and_range():
    o = Oracle()
    player = 'X'
    for board in example_boards:
        score = o.advantage(board, player)
        assert type(score) in [int, float]
        assert score >= 0
        assert score <= 100
