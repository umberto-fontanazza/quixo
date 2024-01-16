from lib.game import Game
from src.agent import Agent
from src.simple_agents import CleverPlayer
from test.example_boards import endgame_1


def main():
    game = Game()
    agent = Agent(tree_depth = 2)
    opponent = CleverPlayer()
    winner = game.play(agent, opponent)
    print(f'{winner =}')
    agent.save(filename = 'trash.json')
    agent.training = False

def main2():
    agent = Agent()
    agent.training = False
    chosen_move = agent.choose_move(
        board = endgame_1,
        current_player = 'X',
        use_multithreading = False)

if __name__ == '__main__':
    main()