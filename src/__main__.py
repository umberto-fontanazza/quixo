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
        if winner_idx == 1:
            wins += 1
        else:
            losses+=1
    print('clever v random:', wins, losses, '\n')

    opponent = CleverPlayer()
    oracle_player = Agent()                       # keep weights learned before
    for depth in range(1, 5):                            # try some different depths, from 1 to 5
        t_0 = time()
        oracle_player.depth_limit = depth
        #oracle_player.training = False
        g = Game()
        players = [oracle_player, opponent]
        starting = 0
        wins, losses = 0, 0
        for _ in range(N_GAMES):
            print('+', end='')
            g = Game()
            winner_idx = g.play(players[starting], players[1-starting])
            agent_won = winner_idx == 0 and starting == 0
            if agent_won:
                wins += 1
            else:
                losses += 1
            starting = 1 -starting
        t_1 = int(time() - t_0)
        unit = 'second(s)' if t_1 < 120 else 'minutes'
        print(f'\ndepth {depth}: {wins} {losses}\t\t( in {t_1 if t_1 < 120 else t_1 / 60} {unit} )\n')

    # match vs human
    """
    # oracle_player.depth_limit = 4
    human_player = ManualPlayer()
    g = Game()
    print(g.play(human_player, oracle_player))
    human_player.print_pretty_board(g)
    """

if __name__ == '__main__':
    main()

