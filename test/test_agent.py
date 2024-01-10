from src.agent import DelphiPlayer, getPossibleMoves
from src.board import random_board, Board
import numpy as np
from itertools import product

import sys                                              # Find a more elegant way for this (?)
sys.path.append('../')
from quixo.lib.game import Game, Move, Player

test_boards = [random_board() for _ in range(10)]

def test_getPossibleMoves():
    # random tests
    for board in test_boards:
        m1, m2 = getPossibleMoves(board, 0), getPossibleMoves(board, 1)
        assert len(m1) + len(m2) > 0
    # test board with no valid moves    
    board = np.array([1] * 25).reshape(5,5)
    assert len(getPossibleMoves(board, 0)) == 0
    #test number of valid moves
    assert len(getPossibleMoves(board, 1)) == (12*3 + 4*2)
    #test should give only 2 doable moves
    board[0, 0] = 0
    assert len(getPossibleMoves(board, 0)) == 2


def test_apply_move():
    #test if a move is applied correctly
    board = np.array([1] * 25).reshape(5,5)
    player = DelphiPlayer()
    player._apply_move(board, ((0, 3), Move.LEFT), 0)
    assert board.sum() == 24
    assert board[0, 0] == 0
    #and another one, unfortunately its not easy to implement ones with a great variablity
    board = np.array([0] * 25).reshape(5,5)
    player = DelphiPlayer()
    player._apply_move(board, ((3, 4), 0), 1)
    assert board.sum() == 1
    assert board[0, 3] == 0
    #nothing should have changed
    board = np.array([1] * 25).reshape(5,5)
    player = DelphiPlayer()
    player._apply_move(board, ((0, 4), 3), 1)
    coord = [0,1,2,3,4]
    for x, y in product(coord, coord):
        assert board[x, y] == 1


from unittest.mock import patch
def test_make_move():
    player = DelphiPlayer()

    # Define the mock function that will replace src.agent.Oracle.advantage
    def mock_oracle_function(b: Board, idx: int):
        return (b[b == idx] + 1).sum()

    #should return a valid move
    with patch('src.agent.Oracle.advantage', side_effect=mock_oracle_function):
        # Inside this block, calls to src.agent.Oracle.advantage will use the mock function
        g = Game()
        result = player.make_move(g)
        assert result[0][0] >= 0 and result[0][0] <= 4
        assert result[0][1] >= 0 and result[0][1] <= 4
        assert result[1] in [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]
        assert result in getPossibleMoves(Game().get_board(), 1)
      
