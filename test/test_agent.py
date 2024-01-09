from src.agent import DelphiPlayer, getPossibleMoves
from src.board import random_board
import numpy as np
from itertools import product

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
    player._apply_move(board, ((0, 4), 3), 0)
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
      
