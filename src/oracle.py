from random import choice
from src.board import Board, Outcome
from src.advisor import Advisor, ALL_ADVISORS

class Oracle():
    def __init__(self, rules: list[Advisor] = ALL_ADVISORS):
        self.__rules = rules

    # TODO: to be implemented
    def feedback(self, game_states: list[Board], outcome: Outcome) -> None:
        raise NotImplementedError()

    def advantage(self, board: Board, player: int) -> float | int:
        advisor_advantages: list[int | float] = [rule(board, player) for rule in self.__rules]
        return sum(advisor_advantages) / len(advisor_advantages) # average