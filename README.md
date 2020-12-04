# MCTS (Monte Carlo Tree Search)
This project comes from a self directed program I implement for Monte Carlo (STA3431). \
The program include two simulation methods for MCTS, and support for various board games like 4x4 Tik-Tak-Toe and Gomoku. \
In the report I have compared two different simulation methods in efficiency and time complexity. The project report is at [Project Link](https://www.wei-siyi.com/files/STA3431_Project_Report.pdf). \
The visualization code was a fork from https://github.com/hayoung-kim/mcts-tic-tac-toe @Hayong-Kim

# Dependencies:
Numpy, Pygame, Matplotlib

# Probability Plots and Game Visualizations

Probability Plots|  Game Visualizations
:-------------------------:|:-------------------------:
![](https://www.wei-siyi.com/images/MCTS_6x6Prob.png)  |  ![](https://www.wei-siyi.com/images/MCTS_6x6Board.png)

# Self Competence between different algorithms
* Please turn off the probability plots before you run the self compete program
* We could see with relatively fewer simulation (around 500 for 4x4 TikTakToe, the improved simulation win 4 of the 10 simulations. and the rest 6 are draw. Which is the optimum result for both winners.)

Time Comparison|  Results
:-------------------------:|:-------------------------:
![](https://www.wei-siyi.com/images/MCTS_TimeComplex.png)  |  ![](https://www.wei-siyi.com/images/MCTS_SCresult.png)

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

# Future working plans
The idea of improving simulation was proven to be inefficient in project report. Thus, the reuse of simulations in previous games should be considered. There are two possible approaches.
* The first approach is to store the tree data structure as the main tree. Then after each iteration, the algorithm will store the new simulation into the tree structure. However, this method is also inefficient intuitively. First it will take massive space complexity. Second, it is a fall back since it works almost the same as greedy algorithm
* The second approach is to construct the distribution of game board entirely. And adjust this distribution to give a reasonable estimation of winning rate. To do this, I want to replace estimation part to neural networks. The neural networks are essentially creating a distribution with numerous parameters. It should suit our purpose well. For generating the simulations. I could use the self competence program.
* Some other technics could be used in generating the datasets. For example, after we generated some datasets with 6x6 Gomoku. We could use the 6x6 board to cover all possible positions on 15x15 boards to generate more datas for 15x15 Gomoku.
