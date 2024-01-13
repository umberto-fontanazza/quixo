from src.oracle import Oracle
from src.board import Board, Outcome
from src.position import Position
from lib.game import Game, Move, Player
from typing import Literal
from src.simple_agents import BetterRandomPlayer

class DelphiPlayer(Player):
    def __init__(self, oracle_weights: list[float] | None = None, tree_depth: int = 4) -> None:
        super().__init__()
        self.__oracle = Oracle(weights = oracle_weights)
        self.__episode: list[Board] = []
        self.__depth_limit: int = tree_depth
        self.player_index = None

    def __max(self, board: Board, current_player: Literal[0,1], beta: float = 100.0, curr_depth: int = 0) -> float:
        #check if the board is a terminal condition
        value = Board.check_for_terminal_conditions(board, current_player)
        if value >= 0:
            return value
        #check if we are above the tree depth limit
        if curr_depth >= self.__depth_limit:
            return self.__oracle.advantage(board, current_player)
        alpha = 0.0                                                 # smallest oracle value
        future_boards: list[Board] = [board.move(move, current_player) for move in board.list_moves(current_player)]
        for b in future_boards:
            tmp = self.__min(b, self.player_index, alpha, curr_depth + 1) # compute the min value for a board
            if tmp > beta:
                return tmp
            alpha = tmp if tmp > alpha else alpha                   # update alpha with the biggest value found so far
        return alpha

    def __min(self, board: Board, current_player: Literal[0,1], alpha: float = 0.0, curr_depth: int = 1) -> float:
        #check if the board is a terminal condition
        value = Board.check_for_terminal_conditions(board, current_player)
        if value >= 0:
            return value
        #check if we are above the tree depth limit
        if curr_depth >= self.__depth_limit:
            return self.__oracle.advantage(board, current_player)
        beta = 100.0                                                # largest oracle value
        future_boards: list[Board] = [board.move(move, current_player) for move in board.list_moves(current_player)]
        for b in future_boards:
            tmp = self.__max(b, self.player_index, beta, curr_depth + 1)
            if tmp < alpha:                                         # if we find a value smaller than alpha we stop and we return this value
                return tmp
            beta = tmp if tmp < beta else beta                      # update beta with the smallest value found so far
        return beta

    def make_move(self, game: Game) -> tuple[tuple[int, int], Move]:
        """Alias is required by lib"""
        position, slide = self.choose_move(game)
        position = position.as_tuple()
        return position, slide

    def choose_move(self, game: Game) -> tuple[Position, Move]:
        """Choose and return a move, without applying it to the board"""
        current_player: Literal[0, 1] = game.get_current_player() # type: ignore
        self.player_index = current_player
        board = Board(game.get_board())
        moves: list[tuple[Position, Move]] =  board.list_moves(current_player) # moves(game.get_board(), current_player)
        future_boards: list[Board] = [board.move(move, current_player) for move in moves]
        evaluated: list[tuple[Board, float, tuple[Position, Move]]] = [(b, self.__min(b, self.player_index), p) for b, p in zip(future_boards, moves)]
        chosen_move: tuple[Board, float, tuple[Position, Move]] = max(evaluated, key = lambda move_qual: move_qual[1])
        self.__episode.append(chosen_move[0])
        return chosen_move[2]

    def train_oracle(self, outcome: Outcome) -> None:
        """at the end of a game, gives feedback to the oracle"""
        player = None # TODO: fill this variable
        self.__oracle.feedback(self.__episode, player, outcome)
        self.__episode = []

    def get_oracle(self) -> Oracle:
        """returns the oracle"""
        return self.__oracle


# TODO: remove this
if __name__ == '__main__':
    # used for testing
    g = Game()

    # informal tests
    if False:
        b = g.get_board()
        for s in BORDERS:
            b[s] = 0
        b[1,0] = 1
        print(b)
        print(len(moves(b, 1)))

    if False:
        b = random_board()
        move: tuple[Position, Move] = ((0, 3), Move.BOTTOM)
        b_after = dp._apply_move(b, move, 1)
        print(f'{b}\n\n{b_after}\n\n')

        import numpy
        b = numpy.array([0] + [1] * 24).reshape((5,5))
        p = moves(b, 0)
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
        p = moves(b, 0)
        #print(p)

    if False:
        print(dp.make_move(g))

    if True:
        from copy import deepcopy

        N_ADVISORS = 4
        initial_weights = ([1.0] * N_ADVISORS)
        player = DelphiPlayer(oracle_weights= initial_weights)
        player1 = BetterRandomPlayer()

        all_weights = []
        for _ in range(5):
            g.play(player, player1)
            won = g.check_winner() == 1
            print(won)
            player.train_oracle('Win' if won else 'Loss')
            all_weights.append(deepcopy(initial_weights))
        print()
        for _ in range(5):
            g.play(player1, player)
            won = g.check_winner() == 0
            print(won)
            player.train_oracle('Win' if won else 'Loss')
            all_weights.append(deepcopy(initial_weights))
        print(all_weights)

    if False:
        b = random_board()
        print(b)
        print(compact_board(b,'X'))

