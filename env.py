# TicTacToe
'''
This is a TicTacToe visualiztion using PyGame
Code has been modified to suit personal use
Author: Siyi Wei

Original Author: KyushikMin kyushikmin@gmail.com
http://mmc.hanyang.ac.kr
'''


import random, sys, time, math, pygame
from pygame.locals import *
import numpy as np
import copy

# Window Information
FPS = 30
WINDOW_WIDTH = 340
WINDOW_HEIGHT = 480
TOP_MARGIN = 100
MARGIN = 20
GAMEBOARD_SIZE = 4
WIN_MARK = 4
GRID_SIZE = WINDOW_WIDTH - 2 * (MARGIN)
MARK_SIZE = GRID_SIZE/(2*GAMEBOARD_SIZE)

HALF_WINDOW_WIDTH = int(WINDOW_WIDTH / 2)
HALF_WINDOW_HEIGHT = int(WINDOW_HEIGHT / 2)

# Colors
#				 R    G    B
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
RED          = (200,  72,  72)
LIGHT_ORANGE = (198, 108,  58)
ORANGE       = (180, 122,  48)
GREEN        = ( 72, 160,  72)
BLUE         = ( 66,  72, 200)
YELLOW       = (162, 162,  42)
NAVY         = ( 75,   0, 130)
PURPLE       = (143,   0, 255)
BADUK        = (220, 179,  92)

def Return_Num_Action():
    return GAMEBOARD_SIZE * GAMEBOARD_SIZE


def Return_BoardParams():
    return GAMEBOARD_SIZE, WIN_MARK


class GameState:
    def __init__(self):
        global FPS_CLOCK, DISPLAYSURF, BASIC_FONT, TITLE_FONT, GAMEOVER_FONT

        pygame.init()
        FPS_CLOCK = pygame.time.Clock()

        DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        pygame.display.set_caption('Board Game')

        BASIC_FONT = pygame.font.Font('freesansbold.ttf', 16)
        TITLE_FONT = pygame.font.Font('freesansbold.ttf', 24)
        GAMEOVER_FONT = pygame.font.Font('freesansbold.ttf', 48)

        # Set initial parameters
        self.init = False
        self.num_mark = 0

        # No stone: 0, Black stone: 1, White stone = -1
        self.gameboard = np.zeros([GAMEBOARD_SIZE, GAMEBOARD_SIZE])

        self.x_win = 0
        self.o_win = 0
        self.count_draw = 0

        # black turn: 0, white turn: 1
        self.turn = 0

        # black wins: 1, white wins: 2, draw: 3, playing: 0
        self.win_index = 0

        # List of X coordinates and Y coordinates
        self.X_coord = []
        self.Y_coord = []

        for i in range(GAMEBOARD_SIZE):
            self.X_coord.append(
                MARGIN + i * int(GRID_SIZE / (GAMEBOARD_SIZE)) + int(
                    GRID_SIZE / (GAMEBOARD_SIZE * 2)))
            self.Y_coord.append(
                TOP_MARGIN + i * int(GRID_SIZE / (GAMEBOARD_SIZE)) + int(
                    GRID_SIZE / (GAMEBOARD_SIZE * 2)))

    def step(self, input_):  # Game loop
        # Initial settings
        if self.init == True:
            self.num_mark = 0

            # No mark: 0, o: 1, x = -1
            self.gameboard = np.zeros([GAMEBOARD_SIZE, GAMEBOARD_SIZE])

            # If O wins
            if self.win_index == 1:
                # x plays first
                self.turn = 1

            # If X wins
            if self.win_index == 2:
                # O plays first
                self.turn = 0

            # Reset init
            self.init = False

        # Key settings
        mouse_pos = 0
        if np.all(input_) == 0 or self.turn == 0:
            # If guide mode of O's turn
            for event in pygame.event.get():  # event loop
                if event.type == QUIT:
                    self.terminate()

                if pygame.mouse.get_pressed()[0]:
                    mouse_pos = pygame.mouse.get_pos()

        # Check mouse position and count
        check_valid_pos = False
        x_index = -1
        y_index = -1

        if mouse_pos != 0:
            for i in range(len(self.X_coord)):
                for j in range(len(self.Y_coord)):
                    if (self.X_coord[i] - 30 < mouse_pos[0] < self.X_coord[
                        i] + 30) and (self.Y_coord[j] - 30 < mouse_pos[1] <
                                              self.Y_coord[j] + 30):
                        check_valid_pos = True
                        x_index = i
                        y_index = j

                        # If selected spot is already occupied, it is not valid move!
                        if self.gameboard[y_index, x_index] == 1 or \
                                        self.gameboard[y_index, x_index] == -1:
                            check_valid_pos = False

        # If vs mode and MCTS works
        if np.any(input_) != 0:
            action_index = np.argmax(input_)
            y_index = int(action_index / GAMEBOARD_SIZE)
            x_index = action_index % GAMEBOARD_SIZE
            check_valid_pos = True

        # Change the gameboard according to the stone's index
        if check_valid_pos:
            if self.turn == 0:
                self.gameboard[y_index, x_index] = 1
                self.turn = 1
                self.num_mark += 1
            else:
                #if(y_index >= self.gameboard.shape[0]): y_index = self.gameboard.shape[0] - 1
                #if(x_index >= self.gameboard.shape[0]): x_index = self.gameboard.shape[0] - 1
                self.gameboard[y_index, x_index] = -1
                self.turn = 0
                self.num_mark += 1

        # Fill background color
        DISPLAYSURF.fill(BLACK)

        # Draw board
        self.draw_main_board()

        # Display Information
        self.title_msg()

        # Display who's turn
        self.turn_msg()

        pygame.display.update()

        # Check_win 0: playing, 1: black win, 2: white win, 3: draw
        self.win_index = self.check_win()
        self.display_win(self.win_index)

        return self.gameboard, check_valid_pos, self.win_index, self.turn

    # Exit the game
    def terminate(self):
        pygame.quit()
        sys.exit()

    # Draw main board
    def draw_main_board(self):
        # Main board size = 400 x 400
        # Game board size = 320 x 320
        # mainboard_rect = pygame.Rect(MARGIN, TOP_MARGIN, WINDOW_WIDTH - 2 * MARGIN, WINDOW_WIDTH - 2 * MARGIN)
        # pygame.draw.rect(DISPLAYSURF, BADUK, mainboard_rect)

        # Horizontal Lines
        for i in range(GAMEBOARD_SIZE + 1):
            pygame.draw.line(DISPLAYSURF, WHITE, (
            MARGIN, TOP_MARGIN + i * int(GRID_SIZE / (GAMEBOARD_SIZE))), (
                             WINDOW_WIDTH - (MARGIN), TOP_MARGIN + i * int(
                                 GRID_SIZE / (GAMEBOARD_SIZE))), 1)

        # Vertical Lines
        for i in range(GAMEBOARD_SIZE + 1):
            pygame.draw.line(DISPLAYSURF, WHITE, (
            MARGIN + i * int(GRID_SIZE / (GAMEBOARD_SIZE)), TOP_MARGIN), (
                             MARGIN + i * int(GRID_SIZE / (GAMEBOARD_SIZE)),
                             TOP_MARGIN + GRID_SIZE), 1)

        # Draw center circle
        pygame.draw.circle(DISPLAYSURF, WHITE, (
        MARGIN + 4 * int(GRID_SIZE / (GAMEBOARD_SIZE)),
        TOP_MARGIN + 4 * int(GRID_SIZE / (GAMEBOARD_SIZE))), 4, 0)

        # Draw marks
        for i in range(self.gameboard.shape[0]):
            for j in range(self.gameboard.shape[1]):
                if self.gameboard[i, j] == 1:
                    pygame.draw.circle(DISPLAYSURF, WHITE,
                                       (self.X_coord[j], self.Y_coord[i]), MARK_SIZE,
                                       0)

                if self.gameboard[i, j] == -1:
                    pygame.draw.line(DISPLAYSURF, WHITE, (
                    self.X_coord[j] - MARK_SIZE, self.Y_coord[i] - MARK_SIZE), (
                                     self.X_coord[j] + MARK_SIZE,
                                     self.Y_coord[i] + MARK_SIZE), 10)
                    pygame.draw.line(DISPLAYSURF, WHITE, (
                    self.X_coord[j] - MARK_SIZE, self.Y_coord[i] + MARK_SIZE), (
                                     self.X_coord[j] + MARK_SIZE,
                                     self.Y_coord[i] - MARK_SIZE), 10)

    # Display title
    def title_msg(self):
        titleSurf = TITLE_FONT.render('Board', True, WHITE)
        titleRect = titleSurf.get_rect()
        titleRect.topleft = (MARGIN, 10)
        DISPLAYSURF.blit(titleSurf, titleRect)

    # Display turn
    def turn_msg(self):
        if self.turn == 0:
            turnSurf = BASIC_FONT.render("O's Turn!", True, WHITE)
            turnRect = turnSurf.get_rect()
            turnRect.topleft = (MARGIN, 60)
            DISPLAYSURF.blit(turnSurf, turnRect)
        else:
            turnSurf = BASIC_FONT.render("X's Turn!", True, WHITE)
            turnRect = turnSurf.get_rect()
            turnRect.topleft = (WINDOW_WIDTH - 75, 60)
            DISPLAYSURF.blit(turnSurf, turnRect)

    # Check win
    def check_win(self):
        """
        get the winner of this board
        arg:
        - board state
        return:
        "o", "x", "draw", None (not ended)
        """
        board = self.gameboard
        win_mark = WIN_MARK

        #return who wins
        def __who_wins(sums, win_mark):
            if np.any(sums == win_mark): return 1
            if np.any(sums == -win_mark): return 2
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
            return 3
        return 0

    # Display Win
    def display_win(self, win_index):
        wait_time = 1
        self.init = False

        # Black Win
        if win_index == 1:
            # Fill background color
            DISPLAYSURF.fill(WHITE)

            winSurf = GAMEOVER_FONT.render("O Win!", True, BLACK)
            winRect = winSurf.get_rect()
            winRect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50)
            DISPLAYSURF.blit(winSurf, winRect)
            pygame.display.update()
            time.sleep(wait_time)

            self.init = True
            self.o_win += 1

        # White Win
        if win_index == 2:
            # Fill background color
            DISPLAYSURF.fill(BLACK)

            winSurf = GAMEOVER_FONT.render("X Win!", True, WHITE)
            winRect = winSurf.get_rect()
            winRect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50)
            DISPLAYSURF.blit(winSurf, winRect)
            pygame.display.update()
            time.sleep(wait_time)

            self.init = True
            self.x_win += 1

        # Draw
        if win_index == 3:
            # Fill background color
            DISPLAYSURF.fill(WHITE)

            winSurf = GAMEOVER_FONT.render("DRAW!", True, BLACK)
            winRect = winSurf.get_rect()
            winRect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50)
            DISPLAYSURF.blit(winSurf, winRect)
            pygame.display.update()
            time.sleep(wait_time)

            self.init = True
            self.count_draw += 1


if __name__ == '__main__':
    main()
