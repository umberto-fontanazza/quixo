from src.board import Board
from numpy import array

board_1 = Board(array([ [-1, -1, -1,  1, -1],
                        [-1, -1, -1, -1, -1],
                        [-1, -1, -1,  0, -1],
                        [-1,  1,  1,  0,  1],
                        [-1, -1, -1,  0, -1]]))

board_2 = Board(array([ [-1,  0,  1,  1,  0],
                        [ 0,  1,  1,  1,  1],
                        [-1, -1, -1, -1,  1],
                        [ 1, -1,  0,  1,  0],
                        [-1,  1,  0,  0, -1]]))

board_3 = Board(array([ [ 0,  1,  0,  0,  0],
                        [ 1,  0,  0,  0,  1],
                        [-1,  1,  0, -1, -1],
                        [-1,  0, -1,  1, -1],
                        [-1,  1,  1,  0, -1]]))

endgame_1 = Board(array([   [ 1,  1,  0,  1,  1],
                            [ 0,  0,  1,  0,  1],
                            [-1,  0,  1,  0,  1],
                            [-1,  0,  0,  1, -1],
                            [-1,  0,  1,  0,  0]]))


example_boards = [Board.random() for _ in range(10)]