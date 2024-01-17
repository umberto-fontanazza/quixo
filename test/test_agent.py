from src.agent import Agent
from src.board import Board
from src.position import Position
from test.example_boards import endgame_1
from lib.game import Game, Move
from unittest.mock import patch

def test_choose_move():
    player = Agent(depth_limit=2)

    # Define the mock function that will replace src.agent.Oracle.advantage
    def mock_oracle_function(board: Board, idx: int):
        return 0

    #should return a valid move
    with patch('src.oracle.Oracle.advantage', side_effect=mock_oracle_function):
        # Inside this block, calls to src.oracle.Oracle.advantage will use the mock function
        g = Game()
        board = Board(g.get_board())
        current_player = 1 if g.get_current_player() else 0
        result = player.choose_move(board, current_player, parallel = True)
        board = Board(g.get_board())
        assert result[0][0] >= 0 and result[0][0] <= 4
        assert result[0][1] >= 0 and result[0][1] <= 4
        assert result[1] in [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]
        assert result in board.list_moves('X')

def test_trivial_choose_move():
    agent = Agent()
    agent.training = False
    chosen_move = agent.choose_move(
        board = endgame_1,
        current_player = 'X')
    assert chosen_move == (Position(4, 2), Move.TOP)