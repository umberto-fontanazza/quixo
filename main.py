from lib.game import Game
from src.agent import DelphiPlayer
from src.simple_agents import CleverPlayer


def main():
    game = Game()
    agent = DelphiPlayer(tree_depth = 2)
    opponent = CleverPlayer()
    winner = game.play(agent, opponent)
    print(f'{winner =}')
    agent.save(filename = 'trash.json')
    agent.training = False

if __name__ == '__main__':
    main()