from src.oracle import Oracle
from src.board import Board, Position, Outcome,get_possible_moves, BORDER_POSITIONS,random_board
from lib.game import Game, Move, Player
from src.advisor import is_legal, compact_board # import for testing
from typing import Literal
import numpy

class DelphiPlayer(Player):
    def __init__(self, tree_depth: int = 4) -> None:
        super().__init__()
        self.__oracle = Oracle()
        self.__episode: list[Board] = []
        self.__depth_limit: int = tree_depth

    def __max(self, board: Board, current_player: Literal[0,1], beta: float = 100.0, curr_depth: int = 0) -> float:
        if curr_depth >= self.__depth_limit:
            return self.__oracle.advantage(board, current_player)
        alpha = 0.0                                                 # smallest oracle value
        future_boards: list[Board] = [self._apply_move(board, p, current_player) for p in get_possible_moves(board, current_player)]
        for b in future_boards:
            tmp = self.__min(b, 0 if current_player == 1 else 1, alpha, curr_depth + 1) # compute the min value for a board
            if tmp > beta:
                return tmp
            alpha = tmp if tmp > alpha else alpha                   # update alpha with the biggest value found so far
        return alpha

    def __min(self, board: Board, current_player: Literal[0,1], alpha: float = 0.0, curr_depth: int = 1) -> float:
        if curr_depth >= self.__depth_limit:
            return self.__oracle.advantage(board, current_player)
        beta = 100.0                                                # largest oracle value
        future_boards: list[Board] = [self._apply_move(board, p, current_player) for p in get_possible_moves(board, current_player)]
        for b in future_boards:
            tmp = self.__max(b, 0 if current_player == 1 else 1, beta, curr_depth + 1)
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

    def __slide(self, board: Board, move: tuple[Position, Move]) -> Board:
        from_pos = move[0]
        slide = move[1]
        axis_0, axis_1 = from_pos
        if slide == Move.RIGHT:
            self._board[axis_0] = numpy.roll(self._board[axis_0], -1)
        elif slide == Move.LEFT:
            self._board[axis_0] = numpy.roll(self._board[axis_0], 1)
        elif slide == Move.BOTTOM:
            self._board[:, axis_1] = numpy.roll(self._board[:, axis_1], -1)
        elif slide == Move.TOP:
            self._board[:, axis_1] = numpy.roll(self._board[:, axis_1], 1)
        return board

    def make_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        current_player: Literal[0, 1] = game.get_current_player()
        moves: list[tuple[Position, Move]] = get_possible_moves(game.get_board(), current_player)
        future_boards: list[Board] = [self._apply_move(game.get_board(), m, current_player) for m in moves]
        evaluated: list[tuple[Board, float, tuple[Position, Move]]] = [(b, self.__min(b, (current_player + 1)%2), p) for b, p in zip(future_boards, moves)]
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
    if False:
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

    if False: #to do change to true
        adv = DelphiPlayer()
        for _ in range(2):
            g.play(dp, adv)
            g.print()
            winner = g.check_winner
            print(winner)
            #dp.feedback('Loss' if winner == 1 else 'Win')
    if True:
        b = random_board()
        print(b)
        print(compact_board(b,'X'))
        
