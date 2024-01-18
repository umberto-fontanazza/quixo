from src.position import Position
from lib.game import Game, Move
from src.simple_agents import BetterRandomPlayer, CleverPlayer, ManualPlayer
from src.agent import Agent
from time import time

def main():
    from tqdm import tqdm

    N_GAMES = 100
    wins, losses = 0, 0
    #baseline random vs random
    for _ in range(N_GAMES):
        g = Game()
        winner_idx = g.play(BetterRandomPlayer(), BetterRandomPlayer())
        if winner_idx == 1:
            wins += 1
        else:
            losses+=1
    print('random v random:', wins, losses)

    wins, losses = 0, 0
    for _ in range(N_GAMES):
        g = Game()
        winner_idx = g.play(CleverPlayer(), BetterRandomPlayer())
        if winner_idx == 0:
            wins += 1
        else:
            losses+=1
    print('clever v random:', wins, losses, '\n')

    opponent = CleverPlayer()
    oracle_player = Agent()                       # keep weights learned before
    for depth in range(1, 4):                            # try some different depths, from 1 to 3
        t_0 = time()
        oracle_player.depth_limit = depth
        #oracle_player.training = False
        g = Game()
        players = [oracle_player, opponent]
        starting = 0
        wins, losses = 0, 0
        for _ in range(N_GAMES):
            g = Game()
            winner_idx = g.play(players[starting], players[1-starting])
            agent_won = (winner_idx == starting)
            print('+' if agent_won else '-', end='')
            if agent_won:
                wins += 1
            else:
                losses += 1
            starting = 1 -starting
        t_1 = int(time() - t_0)
        unit = 'seconds' if t_1 < 120 else 'minutes'
        print(f'\ndepth {depth}: {wins} {losses}\t\t( in {t_1 if t_1 < 120 else t_1 / 60} {unit} )\n')
    oracle_player.to_json()

    # use the learned weights to play at depth 4 without training anymore
    t_0 = time()
    players = [oracle_player, opponent]
    oracle_player.training = False
    oracle_player.depth_limit = 4
    wins, losses = 0, 0
    for _ in range(N_GAMES):
        starting = 0
        g = Game()
        winner_idx = g.play(players[starting], players[1-starting])
        agent_won = (winner_idx == starting)
        print('+' if agent_won else '-', end='')
        if agent_won:
            wins += 1
        else:
            losses += 1
        starting = 1 -starting
    t_1 = int(time() - t_0)
    unit = 'seconds' if t_1 < 120 else 'minutes'
    print(f'\ndepth 4, learned weights: {wins} {losses}\t\t( in {t_1 if t_1 < 120 else t_1 / 60} {unit} )\n')

    oracle_player.to_json()

    # match vs human
    """
    # oracle_player.depth_limit = 4
    human_player = ManualPlayer()
    g = Game()
    print(g.play(human_player, oracle_player))
    human_player.print_pretty_board(g)
    """

def main2():
    from test.example_boards import endgame_1
    agent = Agent()
    agent.training = False
    chosen_move = agent.choose_move(
        board = endgame_1,
        current_player = 1)
    print(endgame_1.ndarray)
    print(chosen_move)

if __name__ == '__main__':
    main()

