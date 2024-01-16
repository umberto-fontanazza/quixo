from lib.game import Game
from src.agent import Agent
from src.simple_agents import CleverPlayer
from test.example_boards import endgame_1


def main():
    agent = Agent(tree_depth=3)
    agent.training = False
    chosen_move = agent.choose_move(
        board = endgame_1,
        current_player = 'X',
        use_multithreading = False)

if __name__ == '__main__':
    main()