from lib.game import Move
from src.board_stats import BoardStats
from src.position import Position
from test.example_boards import board_1, board_2
from numpy import all, array

def test_apply_move_type():
    move = Position(0, 3), Move.LEFT
    actual_result = BoardStats(array = board_1.ndarray).move(move, 'X').ndarray
    expected_result = array([
        [ 1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, -1,  0, -1],
        [-1,  1,  1,  0,  1],
        [-1, -1, -1,  0, -1]])
    assert (actual_result == expected_result).all()

def test_stats_empty_board():
    empty_stats = BoardStats().all_stats
    assert empty_stats == [
        (0,0,4),
        (44,44,44),
        (0,0,9),
        (0,0,25)
    ]

def test_stats_upper_limit():
    move = Position(0, 3), Move.RIGHT
    changed_stats = BoardStats().move(move, 'X').all_stats
    for stat in changed_stats:
        assert stat[0] <= stat[-1]
        assert stat[1] <= stat[-1]

def test_apply_move_stats():
    move = Position(0, 3), Move.LEFT
    changed_stats = BoardStats().move(move, 'X').all_stats
    assert changed_stats == [
        (0,1,4),
        (42,44,44),
        (0,0,9),
        (0,1,25)
    ]

def test_recompute_stats():
    b = BoardStats(array = board_2.ndarray)
    stats = b.all_stats
    print(b.ndarray)
    assert stats == [
        (1, 0, 4),
        (26, 27, 44),
        (1, 4, 9),
        (7, 10, 25)
        ]
