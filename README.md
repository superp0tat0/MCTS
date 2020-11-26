# MCTS (Monte Carlo Tree Search)
This project comes from a self directed program I implement for Monte Carlo (STA3431). \
The project report is at [Project Link](https://www.wei-siyi.com/files/STA3431_Project_Report.pdf) \
The visualization code was a fork from https://github.com/hayoung-kim/mcts-tic-tac-toe @Hayong-Kim

# Quick Start
```
python3 play.py
```

# More parameters
* In env.py you could adjust the board size and how many chess in a line is the winner.
* In play.py you could set AI VS AI for more statistics. ( I am gonna use this part to generate data for training for next step)
* In play.py you could set mcts = MCTS(..., IS=False) to turn off the improved algorithm. The default sampling method is RollOut policy. (Uniform randomly sampling)
* In play.py you could set mcts = MCTS(iterations=400,...) to set the amount of simulations for each step.
* In play.py you could set mcts = MCTS(max_depth=30,...) to set the maximum tree depth for the simulation. Simulation need to have less steps than max_depth to end.
