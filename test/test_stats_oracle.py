from src.stats_oracle import StatsOracle
from src.board_stats import BoardStats
from test.example_boards import example_boards

def test_oracle_advantage_type_and_range():
    s_o = StatsOracle()
    player = 'X'
    for board in example_boards:
        stat_board = BoardStats(array=board.ndarray)
        score = s_o.advantage(stat_board, player)
        assert type(score) in [int, float]
        assert score >= 0
        assert score <= 100
    player = 'O'
    for board in example_boards:
        stat_board = BoardStats(array=board.ndarray)
        score = s_o.advantage(stat_board, player)
        assert type(score) in [int, float]
        assert score >= 0
        assert score <= 100
