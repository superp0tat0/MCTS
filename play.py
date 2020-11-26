import env as game
import numpy as np
from MCTS import MCTS
from MCTS import get_winners
import time
import matplotlib.pyplot as plt



env = game.GameState()
state_size, win_mark = game.Return_BoardParams()
board_shape = [state_size, state_size]
game_board = np.zeros(board_shape, dtype=int)

game_end = False
whos_turn = {0: 'o', 1: 'x'}
mcts_player = 'x' #-1
current_player = 'o' #1

steptime = []


#Human VS algorithms
while not game_end:
    action_onehot = 0
    if current_player == mcts_player:
        mcts = MCTS(iterations=50, max_depth=20, win_mark=win_mark, game_board=game_board, player=current_player)
        best_action, best_q, depth, run_time = mcts.run()
        action_onehot = np.zeros([state_size**2])
        action_onehot[best_action] = 1
        calculate_mcts = False
        steptime.append(run_time)

    # take action and get game info
    game_board, check_valid_position, win_index, turn = env.step(action_onehot)
    current_player = whos_turn[turn]

    if win_index != 0:
        game_board = np.zeros(board_shape, dtype=int)
        plt.plot(steptime)
        plt.ylabel('Improved MCTS runtime per seconds')
        plt.show()
        time.sleep(0.1)
        steptime = []
"""
"""


#Self Competence Program Code
"""
steptime_ISMC = []
steptime_NMC = []
meantime_ISMC = []
meantime_NMC = []

current_player = 1
mcts_player = -1
win_count = [0,0,0]
whos_turn = {'o': 0, 'x': 1, "draw":2}
counter = 0

#Self Competence
while not game_end:
    action_onehot = 0
    if current_player == mcts_player: #IS MC player
        mcts = MCTS(iterations=400, max_depth=30, win_mark=win_mark, game_board=game_board, player=current_player)
        best_action, best_q, depth, run_time = mcts.run(self_compete=True)
        steptime_ISMC.append(run_time)
        game_board[best_action] = -1
    else: #Naive MC player
        mcts = MCTS(iterations=400, max_depth=30, win_mark=win_mark, game_board=game_board, player=current_player, IS=False)
        best_action, best_q, depth, run_time = mcts.run(self_compete=True)
        steptime_NMC.append(run_time)
        game_board[best_action] = 1
    
    print(game_board)
    winner = get_winners(game_board, win_mark)
    current_player = -current_player

    if winner != None:
        win_count[whos_turn[winner]] += 1
        print("guess who is the winner?")
        print(winner)
        print(win_count)
        print(np.mean(steptime_ISMC), np.mean(steptime_NMC))
        meantime_ISMC.append(np.mean(steptime_ISMC))
        meantime_NMC.append(np.mean(steptime_NMC))
        counter += 1
        if(counter % 2 == 1): current_player = 1
        else: current_player = -1

        if(counter == 30):
            #Print the time complexity
            plt.plot(meantime_ISMC, label = "Improved MC")
            plt.plot(meantime_NMC, label = "Naive MC")
            plt.ylabel('Average runtime')
            plt.title("Runtime difference include distribution construction")
            plt.legend()
            plt.show()

        game_board = np.zeros(board_shape, dtype=int)
        steptime_NMC, steptime_ISMC = [], []
        
        time.sleep(0.1)
"""
