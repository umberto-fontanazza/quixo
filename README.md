# Manual
Execute terminal commands from the top level directory quixo.
Testing: {pytest test}
Speed evaluation: {python -m benchmark.speed}


# QUIXO AGENT

oracle asks the advisors for scores
advisors give out scores based on the state of the game
oracle training:
 - for each state and advisor save the score
 - in the end update the weights

 # IMPORTANT REMINDER
 -1 = empty cell
 0  = O
 1  = X

# ideas
saving in the state just the border cells and the two diagonals makes the problem tractable with reinforcement learning

# TODO:
    - refactor agent.__train()
    - add oracle.save(), oracle.load(file)
    - kill repeated calculations for advisors
    - separate rotations from symmetry axes
    - shut off rules with low incidence to speed up oracle predictions
    - benchmark alternative implementations of Position.is_conrner() and Position.is_border()