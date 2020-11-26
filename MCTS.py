import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
import time

class node():
    def __init__(self, parent, board, player, action = None, n = 0, w = 0, q = 0):
        self.child = {} # The child of this node
        self.parent = parent # The parent of this node
        self.board = board # THe game board (nxn np array) of this board)
        self.player = player # Current player of this board state (Who should play at this step)
        self.action = action # The action that could get you from previous board to the current board
        self.n = n # The times this node getting visited
        self.w = w # The times this node wins (updated from the child node)
        self.q = q # The winning rate

def get_winners(board, win_mark):
    """
    get the winner of this board
    arg:
    - board state
    return:
    "o", "x", "draw", None (not ended)
    """

    #return who wins
    def __who_wins(sums, win_mark):
        if np.any(sums == win_mark): return 'o'
        if np.any(sums == -win_mark): return 'x'
        return None

    #jusify the winner of tictactoe
    def __is_terminal_in_conv(leaf_state, win_mark):
        # check row/col
        for axis in range(2):
            sums = np.sum(leaf_state, axis=axis)
            result = __who_wins(sums, win_mark)
            if result is not None: return result
        # check diagonal
        for order in [-1,1]:
            diags_sum = np.sum(np.diag(leaf_state[::order]))
            result = __who_wins(diags_sum, win_mark)
            if result is not None: return result
        return None

    n_rows_board = len(board)
    window_positions = range(n_rows_board - win_mark + 1)

    #Jusify the winner looping board by win_mark 
    for row in window_positions:
        for col in window_positions:
            window = board[row:row+win_mark, col:col+win_mark]
            winner = __is_terminal_in_conv(window, win_mark)
            if winner is not None:
                return winner

    if not np.any(board == 0):
        return 'draw'
    return None

def get_valid_actions(board, timer = False):
    '''
    return all possible action in current leaf state
    in:
    - board
    out:
    - set of possible actions (row,col) - start from 0
    '''
    start_time = time.time()
    actions = []
    state_size = len(board)

    for i in range(state_size):
        for j in range(state_size):
            if board[i][j] == 0:
                actions.append((i, j))
    runtime = time.time() - start_time

    if(timer): return actions, runtime
    else: return actions, 0

def get_neighbor_actions(board, timer = False):
    '''
    return all neighbot actions in current leaf state
    in:
    - board
    out:
    - set of possible actions (row,col) - start from 0
    '''
    start_time = time.time()
    actions = set()
    valid_actions, _ = get_valid_actions(board)
    state_size = len(board)

    for i in range(state_size):
        for j in range(state_size):
            if board[i][j] != 0:
                for index_a in range(i-1, i+2):
                    for index_b in range(j-1,j+2):
                        if((index_a, index_b) in valid_actions):
                            actions.add((index_a, index_b))
    run_time = time.time() - start_time

    if(timer): return list(actions), run_time
    else: return list(actions), 0


class MCTS(object):
    def __init__(self, iterations=100, max_depth=5, game_board=None, win_mark=3, player=None, explore_constant=np.sqrt(2), IS = True):
        self.iterations = iterations
        self.max_depth = max_depth
        self.explore_constant = explore_constant

        self.win_mark = win_mark
        self.game_board = game_board
        self.player = player
        self.total_n = 0

        self.size = len(game_board)
        
        self.tree = node(None, self.game_board, self.player)
        self.IS = IS #Importance sampling on / off

    def select(self):
        """
        Select the next node for expansion
        """
        node_founded = False
        current_node = self.tree
        depth = 0
        
        while not node_founded:
            child_nodes = current_node.child
            depth += 1

            if(len(child_nodes) == 0): #If this node is not yet explored
                node_founded = True
            else:                     #Else, select one from the child (UCT) node and keep searching
                max_uct_value = -100.0
                for child_node in child_nodes:
                    w = child_node.w
                    n = child_node.n
                    total_n = self.total_n
                    if(n == 0): n = 1e-4 #Avoid numerical error

                    #UCT formula
                    exploitation_value = w / n
                    exploration_value  = np.sqrt(np.log(total_n)/n)
                    uct_value = exploitation_value + self.explore_constant * exploration_value

                    if uct_value > max_uct_value:
                        max_uct_value = uct_value
                        current_node = child_node
        return depth, current_node

    def expand(self, leaf_node):
        """
        Expand the current node
        """
        leaf_board = leaf_node.board
        winner = get_winners(leaf_board, self.win_mark)
        avaliable_actions, _ = get_valid_actions(leaf_board)

        current_node = leaf_node
        if (winner is None): # Not a terminal state
            avaliable_childs = []
            for action in avaliable_actions: #Grow all the avaliable actions
                board = deepcopy(leaf_node.board)
                current_player = leaf_node.player

                if(current_player == 'o'):
                    next_player = 'x'
                    board[action] = 1
                else:
                    next_player = 'o'
                    board[action] = -1

                new_child = node(current_node, board, next_player, action=action)
                avaliable_childs.append(new_child)
            current_node.child = avaliable_childs
            random_index = np.random.randint(low=0, high=len(avaliable_childs), size=1)
            current_node = avaliable_childs[random_index[0]]
        
        return current_node 


    def simulate(self, child_node):
        self.total_n += 1
        board = deepcopy(child_node.board)
        previous_player = child_node.player
        winner = get_winners(board, self.win_mark)
        simulate_time = 0

        while(winner is None):
            if(self.IS): avaliable_actions, runtime = get_neighbor_actions(board, False) #Improved MCTS
            else: avaliable_actions, runtime = get_valid_actions(board, False) #Naive MCTS

            #Roll out trick random assign the chesses
            random_index = np.random.randint(low=0, high=len(avaliable_actions), size=1)[0]
            action = avaliable_actions[random_index]
            simulate_time += runtime

            if previous_player == 'o':
                current_player = 'x'
                board[action] = -1
            else:
                current_player = 'o'
                board[action] = 1
            
            previous_player = current_player
            winner = get_winners(board, self.win_mark)
        
        return winner, simulate_time

    def backprop(self, child_node, winner):
        player = self.tree.player

        if(winner == "draw"):
            reward = 0
        elif(winner == player):
            reward = 1
        else:
            reward = -1
        
        #Update gaming info from child node all the way to the root node
        finished = False
        while(not finished):
            child_node.n += 1
            child_node.w += reward
            child_node.q = child_node.w / child_node.n 
            parent_node = child_node.parent
            if(parent_node is not None):
                child_node = parent_node
            else:
                finished = True

    def run(self, self_compete = False): #Self compete on/off, the return type is different.
        start_time = time.time()
        simulate_time = 0

        for i in range(self.iterations):
            #if(i % 300 == 1): print(".")
            depth, selected_node = self.select()
            child_node = self.expand(selected_node)
            winner, runtime = self.simulate(child_node)
            simulate_time += runtime

            self.backprop(child_node, winner)

            if(depth > self.max_depth): #If depth over max depth, kill the loop and assess based on current information
                break
        
        #Select the best action
        current_node = self.tree
        possible_nodes = current_node.child
        best_q = -100
        for node in possible_nodes:
            #print(q, node.action)
            if(node.q > best_q):
                best_q = node.q
                best_action = node.action
        #print("----------------------------")
        self.p_plot(possible_nodes) #Probability plots
        run_time = time.time() - start_time - simulate_time

        if(not self_compete): #Visulization require int action type
            best_action = best_action[0] * self.size + best_action[1]

        return best_action, best_q, depth, run_time
            
    def p_plot(self, possible_nodes):
        # The winning probability plots
        fig = plt.figure(figsize=(6,6))
        for node in possible_nodes:
            _state = deepcopy(node.board)
            _q = node.q
            a = node.action[0] * self.size + node.action[1]

            plt.subplot(len(_state),len(_state),a+1)
            plt.pcolormesh(_state, alpha=0.7, cmap="RdBu")
            plt.axis('equal')
            plt.gca().invert_yaxis()
            plt.xticks([], [])
            plt.yticks([], [])
            plt.title('[%d] P=%.2f' % (a,(_q+1)/2))
        plt.draw()
        plt.waitforbuttonpress(0)
        plt.close(fig)

if(__name__ == "__main__"):
    board = np.array([[1,1,1,1,0,-1], [-1,-1,-1,-1,-1,0], [0,0,0,0,0,0], [0,0,0,0,0,1], [0,0,0,0,0,1], [0,0,0,0,1,0]])
    print(get_winners(board, win_mark=5))