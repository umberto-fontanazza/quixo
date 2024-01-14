from src.position import Position
from lib.game import Game, Move
from src.simple_agents import BetterRandomPlayer, CleverPlayer
from src.agent import DelphiPlayer

def main():
    g = Game()
    from tqdm import tqdm

    N_ADVISORS = 4
    initial_weights = ([1.0] * N_ADVISORS)
    oracle_player = DelphiPlayer(tree_depth=4, oracle_weights= initial_weights)
    opponent = CleverPlayer()
    N_GAMES = 100
    wins, losses = 0, 0
    #baseline random vs random
    for _ in range(N_GAMES):
        winner_idx = g.play(BetterRandomPlayer(), BetterRandomPlayer())
        if winner_idx == 1:
            wins += 1
        else:
            losses+=1
    print('random v random:', wins, losses)

    wins, losses = 0, 0
    for _ in range(N_GAMES):
        winner_idx = g.play(opponent, CleverPlayer())
        if winner_idx == 1:
            wins += 1
        else:
            losses+=1
    print('clever v random:', wins, losses)
    for depth in range(1, 5):                            #try some different depths, from 1 to 5
        oracle_player = DelphiPlayer(tree_depth=depth)
        #oracle_player.training = False
        players = [oracle_player, opponent]
        starting = 0
        wins, losses = 0, 0
        for _ in tqdm(range(N_GAMES)):
            winner_idx = g.play(players[starting], players[1-starting])
            agent_won = winner_idx == 0 and starting == 0
            if agent_won:
                wins += 1
            else:
                losses += 1
        print('depth', depth, ':', wins, losses)
        starting = 1 if starting == 0 else 0

if __name__ == '__main__':
    main()

