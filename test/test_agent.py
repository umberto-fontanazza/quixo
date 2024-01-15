from src.agent import DelphiPlayer
from src.board import Board
from lib.game import Game, Move
from unittest.mock import patch

def test_choose_move():
    player = DelphiPlayer(tree_depth=2)

    # Define the mock function that will replace src.agent.Oracle.advantage
    def mock_oracle_function(board: Board, idx: int):
        return 0

    #should return a valid move
    with patch('src.oracle.Oracle.advantage', side_effect=mock_oracle_function):
        # Inside this block, calls to src.oracle.Oracle.advantage will use the mock function
        g = Game()
        result = player.choose_move(g, use_multithreading=True)
        board = Board(g.get_board())
        assert result[0][0] >= 0 and result[0][0] <= 4
        assert result[0][1] >= 0 and result[0][1] <= 4
        assert result[1] in [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]
        assert result in board.list_moves('X')