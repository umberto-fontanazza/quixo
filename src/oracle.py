from src.board import Board, Player, Outcome
from src.advisor import Advisor, ALL_ADVISORS

class Oracle():
    def __init__(self, rules: list[Advisor] = ALL_ADVISORS, weights: list[float] | None = None):
        self.__rules = rules
        if not weights or len(weights) != len(rules):
            self.__weights = [1 for _ in rules]
        else:
            self.__weights = weights

    @staticmethod
    def __is_good_prediction(score: float, outcome: Outcome) -> bool:
        if score >= 50 and outcome == 'Win':
            return True
        if score < 50 and outcome == 'Loss':
            return True
        return False

    def __adjust_rule_weights(self, board: Board, player: Player, outcome: Outcome):
        growth_factor = .1
        shrink_factor = .1
        rule_scores: list[float] = [rule(board, player) for rule in self.__rules]
        rule_success = [self.__is_good_prediction(score, outcome) for score in rule_scores]
        for success, weight in zip(rule_success, self.__weights):
            if success:
                weight += weight * growth_factor
            else:
                weight -= weight * shrink_factor

    def feedback(self, board_states: list[Board], player: Player, outcome: Outcome) -> None:
        for board in board_states:
            self.__adjust_rule_weights(board, player, outcome)

    def advantage(self, board: Board, player: Player) -> float:
        advisor_advantages: list[float] = [rule(board, player) for rule in self.__rules]
        total_score = 0
        for i, rule_score in enumerate(advisor_advantages):
            rule_weight = self.__weights[i]
            total_score += rule_score *  rule_weight
        return total_score / sum(self.__weights)