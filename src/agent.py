from src.oracle import Oracle
from src.board import Board, Position, Outcome
from lib.game import Game, Move, Player
from typing import Literal
import numpy

"""To run use python -m src.agent from root dir"""
# import sys                                              # Find a more elegant way for this (?)
# sys.path.append('../')
# from quixo.lib.game import Game, Move, Player

SLIDES = [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]
BORDER_POSITIONS = [(x, y) for x in range(5) for y in [0, 4]] + [(x, y) for x in [0, 4] for y in range(1, 4)]

def get_possible_moves(board: Board, idx: int) -> list[tuple[Position, Move]]:
    """returns all the possible moves given a Game object
        that is, a list of tuples (Position, Move)"""
    possible = []
    for p in BORDER_POSITIONS:
        if board[p] == -1 or board[p] == idx:                                #if it is blank (-1) or mine (idx)
            if p[0] == 0:                                                    #in the top row
                if p[1] == 0:
                    possible += [(p, Move.BOTTOM), (p, Move.RIGHT)]
                elif p[1] == 4:
                    possible += [(p, Move.BOTTOM), (p, Move.LEFT)]
                else:
                    possible += [(p, Move.BOTTOM), (p, Move.LEFT), (p, Move.RIGHT)]
            elif p[0] == 4:
                if p[1] == 0:
                    possible += [(p, Move.TOP), (p, Move.RIGHT)]            #in the bottom row
                elif p[1] == 4:
                    possible += [(p, Move.TOP), (p, Move.LEFT)]
                else:
                    possible += [(p, Move.TOP), (p, Move.LEFT), (p, Move.RIGHT)]
            elif p[1] == 0:                                                 #other rows (1,2,3) on left side
                possible += [(p, Move.TOP), (p, Move.BOTTOM), (p, Move.RIGHT)]
            else:                                                           #other rows on right side
                possible += [(p, Move.TOP), (p, Move.LEFT), (p, Move.BOTTOM)]
    # i know, it is going to be evaluated again by game, but i think we could really save up some time
    numpy.random.shuffle(possible)
    return possible


class DelphiPlayer(Player):
    def __init__(self, tree_depth: int = 4) -> None:
        super().__init__()
        self.__oracle = Oracle()
        self.__episode: list[Board] = []
        self.__depth_limit: int = tree_depth

    def __max(self, board: Board, idx: Literal[0,1], beta: float = 100.0, curr_depth: int = 0) -> float:
        if curr_depth >= self.__depth_limit:
            return self.__oracle.advantage(board, idx)
        alpha = 0.0                                                 # smallest oracle value
        future_boards: list[Board] = [self._apply_move(board, p, idx) for p in get_possible_moves(board, idx)]
        for b in future_boards:
            tmp = self.__min(b, (idx + 1) % 2, alpha, curr_depth + 1) # compute the min value for a board
            if tmp > beta:
                return tmp
            alpha = tmp if tmp > alpha else alpha                   # update alpha with the biggest value found so far
        return alpha

    def __min(self, board: Board, idx: Literal[0,1], alpha: float = 0.0, curr_depth: int = 1) -> float:
        if curr_depth >= self.__depth_limit:
            return self.__oracle.advantage(board, idx)
        beta = 100.0                                                # largest oracle value
        future_boards: list[Board] = [self._apply_move(board, p, idx) for p in get_possible_moves(board, idx)]
        for b in future_boards:
            tmp = self.__max(b, (idx + 1) % 2, beta, curr_depth + 1)
            if tmp < alpha:                                         # if we find a value smaller than alpha we stop and we return this value
                return tmp
            beta = tmp if tmp < beta else beta                      # update beta
        return beta

    def _apply_move(self, boardcopy: Board, move: tuple[Position, Move], idx: int) -> Board:
        """apllies move to the board and returns it
            given a board, a valid move and the player index
            valid move should be one generated by getPossibleMoves"""
        boardcopy[move[0]] = idx                            # take the piece
        return self.__slide(boardcopy, move)                # slide the pieces

    # TODO: test, i copied from the game.py and adapted it
    def __slide(self, board: Board, move: tuple[Position, Move]):
        from_pos = move[0]
        slide = move[1]
        piece = board[from_pos]
        # if the player wants to slide it to the left
        if slide == Move.LEFT:
            # for each column starting from the column of the piece and moving to the left
            for i in range(from_pos[1], 0, -1):
            # copy the value contained in the same row and the previous column
                board[(from_pos[0], i)] = board[(
                    from_pos[0], i - 1)]
            # move the piece to the left
            board[(from_pos[0], 0)] = piece
        # if the player wants to slide it to the right
        elif slide == Move.RIGHT:
            # for each column starting from the column of the piece and moving to the right
            for i in range(from_pos[1], board.shape[1] - 1, 1):
                # copy the value contained in the same row and the following column
                board[(from_pos[0], i)] = board[(
                    from_pos[0], i + 1)]
            # move the piece to the right
            board[(from_pos[0], board.shape[1] - 1)] = piece
        # if the player wants to slide it upward
        elif slide == Move.TOP:
            # for each row starting from the row of the piece and going upward
            for i in range(from_pos[0], 0, -1):
                # copy the value contained in the same column and the previous row
                board[(i, from_pos[1])] = board[(
                    i - 1, from_pos[1])]
            # move the piece up
            board[(0, from_pos[1])] = piece
        # if the player wants to slide it downward
        elif slide == Move.BOTTOM:
            # for each row starting from the row of the piece and going downward
            for i in range(from_pos[0], board.shape[0] - 1, 1):
                # copy the value contained in the same column and the following row
                board[(i, from_pos[1])] = board[(
                    i + 1, from_pos[1])]
            # move the piece down
            board[(board.shape[0] - 1, from_pos[1])] = piece
        return board

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        idx: int = game.get_current_player()
        moves: list[tuple[Position, Move]] = get_possible_moves(game.get_board(), idx)
        future_boards: list[Board] = [self._apply_move(game.get_board(), m, idx) for m in moves]
        evaluated: list[tuple[Board, float, tuple[Position, Move]]] = [(b, self.__min(b, (idx + 1)%2), p) for b, p in zip(future_boards, moves)]
        chosen_move: tuple[Board, float, tuple[Position, Move]] = max(evaluated, key = lambda move_qual: move_qual[1])
        self.__episode.append(chosen_move[0])
        return chosen_move[2]

    def train_oracle(self, outcome: Outcome) -> None:
        """at the end of a game, gives feedback to the oracle"""
        player = None
        self.__oracle.feedback(self.__episode, player, outcome) # TODO: add player @arg
        self.__episode = []



# TODO: remove this
if __name__ == '__main__':
    # used for testing

    dp = DelphiPlayer()
    g = Game()

    # informal tests
    if True:
        b = g.get_board()
        for s in BORDER_POSITIONS:
            b[s] = 0
        b[1,0] = 1
        print(b)
        print(len(get_possible_moves(b, 1)))

    if False:
        b = random_board()
        move: tuple[Position, Move] = ((0, 3), Move.BOTTOM)
        b_after = dp._apply_move(b, move, 1)
        print(f'{b}\n\n{b_after}\n\n')

        import numpy
        b = numpy.array([0] + [1] * 24).reshape((5,5))
        p = get_possible_moves(b, 0)
        #print(p)

        b = numpy.array([1] * 24 + [0]).reshape((5,5))
        b_after = dp._apply_move(b, ((4,3), Move.LEFT), 0)
        print(f'\n\n{b_after}\n\n')
        b = numpy.array([1] * 25).reshape((5,5))
        b_after = dp._apply_move(b, ((3,4), Move.LEFT), 0)
        print(f'\n\n{b_after}\n\n')
        b_after[3, 0] = 1
        b_after[0, 1] = 0
        print(f'{b_after}\n\n')


        b = numpy.array([1] * 24 + [0]).reshape((5,5))
        p = get_possible_moves(b, 0)
        #print(p)

    if False:
        print(dp.make_move(g))

    if True:
        adv = DelphiPlayer()
        for _ in range(2):
            g.play(dp, adv)
            g.print()
            winner = g.check_winner
            print(winner)
            #dp.feedback('Loss' if winner == 1 else 'Win')