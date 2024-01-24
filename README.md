# Quixo project
Quixo project done by:
Fiorio Ludovico s306058
Fontanazza Umberto s323916
Ricatto Alberto s309141
For the 2024 winter session of the Computational Intelligence course exam

# Manual
Execute terminal commands from the top level directory quixo.
Testing: {pytest test}
Speed evaluation: {python -m benchmark.speed}


# QUIXO AGENT

oracle uses the board stats as scores
in the original idea, advisors gave out scores based on the state of the game
oracle training:
 - for each state and state save the score
 - in the end update the weights (using a shrink / growth factor)

There are also 3 bonus agents to play with (src/simple_agents.py):
 - BetterRandomPlayer, makes random but legal moves
 - CleverPlayer, makes random moves, but if it has the possibility to win chooses that move and does not make the opponent win with its move
 - ManualPlayer, shows the board and asks the user to choose a move

For a demonstration, use the ```__main__``` file in quixo/lib directoy using the command:
 - ```python -m lib```
 - executing it from your ```quixo``` directory
For a more in-depth analysis you can execute:
 - ```python -m src```
 - always from your ```quixo``` directory


# CONSIDERATIONS

Agent at depth 3 is enjoyable in a human amount of time (abt. 5 seconds) and is already very good against a Random / Clever.
If it was to play against a human player, depth = 4 or 5 may be more appropriate (Alberto could not beat depth 4)
We saw that the GOOD_WEIGHTS, after training at depth 1,2,3 for 100 games each (oracle lr = 0.001), work well also when playing at depth 4 or 5.




## SPARE STUFF
### ideas
saving in the state just the border cells and the two diagonals makes the problem tractable with reinforcement learning

### TODO:
    - kill repeated calculations for advisors
    - separate rotations from symmetry axes
    - shut off rules with low incidence to speed up oracle predictions
    - benchmark alternative implementations of Position.is_conrner() and Position.is_border()