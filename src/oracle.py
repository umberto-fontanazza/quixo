from src.board import Board, Player, Outcome
from src.advisor import Advisor, ALL_ADVISORS

class Oracle():
    def __init__(self, rules: list[Advisor] = ALL_ADVISORS, weights: list[float] | None = None):
        self.__rules = rules
        if not weights or len(weights) != len(rules):
            self.__weights = [1 for _ in rules]
        else:
            self.__weights = weights

    def __adjust(self, board: Board, Outcome):
        raise NotImplementedError()

    # TODO: to be implemented
    def feedback(self, game_states: list[Board], outcome: Outcome) -> None:
        raise NotImplementedError()

    def advantage(self, board: Board, player: Player) -> float:
        advisor_advantages: list[float] = [rule(board, player) for rule in self.__rules]
        total_score = 0
        for i, rule_score in enumerate(advisor_advantages):
            rule_weight = self.__weights[i]
            total_score += rule_score *  rule_weight
        return total_score / sum(self.__weights)