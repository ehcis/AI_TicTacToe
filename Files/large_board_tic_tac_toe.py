#cSpell:ignore pygame negamax mousebuttondown mousebuttonup collidepoint tictactoegame

import pygame
import numpy as np
import math
from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax
import sys, random
import copy


class RandomBoardTicTacToe:
    def __init__(self, size = (600, 600)):

        self.size = self.width, self.height = size
        # Define some colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.GRAY = (96, 118, 143)

        # Grid Size
        self.GRID_SIZE = 4
        self. OFFSET = 5

        self.CIRCLE_COLOR = (140, 146, 172)
        self.CROSS_COLOR = (140, 146, 172)

        # This sets the WIDTH and HEIGHT of each grid location
        self.WIDTH = self.size[0]/self.GRID_SIZE - self.OFFSET
        self.HEIGHT = self.size[1]/self.GRID_SIZE - self.OFFSET

        # This sets the margin between each cell
        self.MARGIN = 5

        # more variables
        self.board = []
        self.clicked = False
        self.pos = []
        self.player = 1 # X = 1, O = -1
        self.turn = 1
        self.ShowMenu = True
        self.mode = "minimax" # default mode for playing the game (player vs AI)
        


        # Initialize pygame
        pygame.init()
        self.font = pygame.font.SysFont(None, 40)
        self.button1 = pygame.Rect(self.width, self.height, 0, 0)
        self.button2 = pygame.Rect(self.width, self.height, 0, 0)
        self.button3 = pygame.Rect(self.width, self.height, 0, 0)
        self.button4 = pygame.Rect(self.width, self.height, 0, 0)
        self.game_reset()

    def draw_game(self):
        # Create a 2 dimensional array using the column and row variables
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Tic Tac Toe Random Grid")
        self.screen.fill(self.BLACK)
        # Draw the grid
        for x in range (self.GRID_SIZE):
            pygame.draw.line(self.screen, self.WHITE, (0, x * (self.width / self.GRID_SIZE)), (self.width, x * (self.width / self.GRID_SIZE)), 6)
            pygame.draw.line(self.screen, self.WHITE, (x * ((self.height) / self.GRID_SIZE), 0), (x * ((self.height) / self.GRID_SIZE), self.height), 6)
        
        pygame.display.update()

    def draw_menu(self):
        #Draw Menu
        pygame.draw.rect(self.screen, self.GRAY, (math.floor(self.width / 2) - 200, math.floor(self.height / 2) - 250, 400, 500))
        menu_img = self.font.render("Menu:", True, self.WHITE)
        self.screen.blit(menu_img, ((self.width // 2) - 100, (self.height // 5)))
        # X or O ------------------------------------------------------------------------
        if self.player == 1:
            playerText = "X"
        else:
            playerText = "O"
        self.button1 = pygame.Rect(self.width // 2 - 80, self.height // 2 - 100, 160, 50)
        pygame.draw.rect(self.screen, self.BLACK, self.button1)
        player_img = self.font.render(playerText, True, self.WHITE)
        self.screen.blit(player_img, (self.width // 2 - 10, self.height // 2 - 100 + 10))
        # Human or AI -------------------------------------------------------------------
        if self.mode == "minimax":
            modeText = "MiniMax"
        elif self.mode == "negamax":
            modeText = "NegaMax"
        elif self.mode == "human":
            modeText = "P v P"
        self.button2 = pygame.Rect(self.width // 2 - 80, self.height // 2 - 20, 160, 50)
        pygame.draw.rect(self.screen, self.BLACK, self.button2)
        mode_img = self.font.render(modeText, True, self.WHITE)
        self.screen.blit(mode_img, (self.width // 2 - 40, self.height // 2 - 20 + 10))
        # Board Size (4x4, 5x5, 6x6) ----------------------------------------------------
        if self.GRID_SIZE == 4:
            sizeText = "4 x 4"
        elif self.GRID_SIZE == 5:
            sizeText = "5 x 5"
        elif self.GRID_SIZE == 6:
            sizeText = "6 x 6"
        self.button3 = pygame.Rect(self.width // 2 - 80, self.height // 2 + 60, 160, 50)
        pygame.draw.rect(self.screen, self.BLACK, self.button3)
        size_img = self.font.render(sizeText, True, self.WHITE)
        self.screen.blit(size_img, (self.width // 2 - 40, self.height // 2 + 60 + 10))
        # Start Game --------------------------------------------------------------------
        self.button4 = pygame.Rect(self.width // 2 - 80, self.height // 2 + 140, 160, 50)
        pygame.draw.rect(self.screen, self.BLACK, self.button4)
        start_img = self.font.render("Start", True, self.GREEN)
        self.screen.blit(start_img, (self.width // 2 - 40, self.height // 2 + 140 + 10))

    def draw_winner(self, score):
        if (score > 0):
            win_text = "Player X Wins!"
        elif (score < 0):
            win_text = "Player O Wins!"
        else:
            win_text = "Draw!"
        #Draw Menu
        pygame.draw.rect(self.screen, self.GRAY, (math.floor(self.width / 2) - 200, math.floor(self.height / 2) - 250, 400, 500))
        #Winner
        win_img = self.font.render(win_text, True, self.GREEN)
        self.screen.blit(win_img, ((self.width // 2) - 100, (self.height // 5)))
        #play again
        self.button1 = pygame.Rect(self.width // 2 - 80, self.height // 2 - 80, 160, 50)
        pygame.draw.rect(self.screen, self.BLACK, self.button1)
        again_img = self.font.render("Play Again", True, self.WHITE)
        self.screen.blit(again_img, (self.width // 2 - 80, self.height // 2 - 80 + 10))
        #menu
        self.button2 = pygame.Rect(self.width // 2 - 80, self.height // 2 + 20, 160, 50)
        pygame.draw.rect(self.screen, self.BLACK, self.button2)
        menu_img = self.font.render("Menu", True, self.WHITE)
        self.screen.blit(menu_img, (self.width // 2 - 80, self.height // 2 + 20 + 10))
        #quit
        self.button3 = pygame.Rect(self.width // 2 - 80, self.height // 2 + 100, 160, 50)
        pygame.draw.rect(self.screen, self.BLACK, self.button3)
        quit_img = self.font.render("Quit", True, self.RED)
        self.screen.blit(quit_img, (self.width // 2 - 80, self.height // 2 + 100 + 10))
        


    def change_turn(self):

        if(self.game_state.turn_O):
            pygame.display.set_caption("Tic Tac Toe - X's turn")
        else:
            pygame.display.set_caption("Tic Tac Toe - O's turn")


    def draw_circle(self, x, y):
        pygame.draw.circle(self.screen, self.CIRCLE_COLOR, (x * (self.width / self.GRID_SIZE) + ((self.width / self.GRID_SIZE) / 2), y * (self.width / self.GRID_SIZE) + ((self.width / self.GRID_SIZE) / 2)), (((self.width / self.GRID_SIZE) / 2) * .75), 6)


    def draw_cross(self, x, y):
        pygame.draw.line(self.screen, self.CROSS_COLOR, (x * (self.width / self.GRID_SIZE) + ((self.width / self.GRID_SIZE) * .15), y * (self.width / self.GRID_SIZE) + ((self.width / self.GRID_SIZE) * .15)), (x * (self.width / self.GRID_SIZE) + ((self.width / self.GRID_SIZE) - ((self.width / self.GRID_SIZE) * .15)), y * (self.width / self.GRID_SIZE) + ((self.width / self.GRID_SIZE) - ((self.width / self.GRID_SIZE) * .15))), 6)
        pygame.draw.line(self.screen, self.CROSS_COLOR, (x * (self.width / self.GRID_SIZE) + ((self.width / self.GRID_SIZE) * .15), y * (self.width / self.GRID_SIZE) + ((self.width / self.GRID_SIZE) - ((self.width / self.GRID_SIZE) * .15))), (x * (self.width / self.GRID_SIZE) + ((self.width / self.GRID_SIZE) - ((self.width / self.GRID_SIZE) * .15)), y * (self.width / self.GRID_SIZE) + ((self.width / self.GRID_SIZE) * .15)), 6)
        

    def is_game_over(self):
        if self.game_state.is_terminal():
            return True
        else:
            return False
    

    def move(self, move):
        self.game_state = self.game_state.get_new_state(move)
        print("board state: ", self.game_state.board_state)
        x, y = move[0], move[1]
        if (self.game_state.turn_O):
            self.draw_circle(x,y)
        else:
            self.draw_cross(x, y)
        self.change_turn()
        if self.is_game_over():
            self.draw_winner(self.game_state.get_scores(True))


    def play_ai(self):
        """
        YOUR CODE HERE TO CALL MINIMAX OR NEGAMAX DEPENDEING ON WHICH ALGORITHM SELECTED FROM THE GUI
        ONCE THE ALGORITHM RETURNS THE BEST MOVE TO BE SELECTED, YOU SHOULD DRAW THE NOUGHT (OR CIRCLE DEPENDING
        ON WHICH SYMBOL YOU SELECTED FOR THE AI PLAYER)
        
        THE RETURN VALUES FROM YOUR MINIMAX/NEGAMAX ALGORITHM SHOULD BE THE SCORE, MOVE WHERE SCORE IS AN INTEGER
        NUMBER AND MOVE IS AN X,Y LOCATION RETURNED BY THE AGENT
        """

        if (self.mode == "minimax"):
            score, move = minimax(copy.deepcopy(self.game_state), 4, True)
        elif (self.mode == "negamax"):
            score, move = negamax(copy.deepcopy(self.game_state), 4, True)
        
        self.move(move)
        
        self.change_turn()
        pygame.display.update()
        terminal = self.game_state.is_terminal()
        """ USE self.game_state.get_scores(terminal) HERE TO COMPUTE AND DISPLAY THE FINAL SCORES """


    def game_reset(self):
        self.draw_game()
        self.board = []
        for x in range(self.GRID_SIZE):
            row = [0] * self.GRID_SIZE
            self.board.append(row)

        self.game_state = GameStatus(self.board, self.player)
        self.change_turn()

        pygame.display.update()


    def play_game(self):
        done = False

        clock = pygame.time.Clock()
        self.draw_menu()

        while not done:
            for event in pygame.event.get():

                # Quits Game
                if event.type == pygame.QUIT:
                    done = True
                
                # Game Over
                if self.is_game_over():
                    
                    self.draw_winner(self.game_state.get_scores(True))
                    if event.type == pygame.MOUSEBUTTONDOWN and self.clicked == False:
                        self.clicked = True
                    if event.type == pygame.MOUSEBUTTONUP and self.clicked == True:
                        self.clicked = False
                        self.pos = pygame.mouse.get_pos()
                        if self.button1.collidepoint(self.pos):
                            print("Re-Play")
                            self.game_reset()
                        if self.button2.collidepoint(self.pos):
                            print("Menu")
                            self.ShowMenu = True
                            self.game_reset()
                            self.draw_menu()
                        if self.button3.collidepoint(self.pos):
                            print("Game Over")
                            done = True
                #play Turns               
                if not self.is_game_over() and not self.ShowMenu:
                    if event.type == pygame.MOUSEBUTTONDOWN and self.clicked == False:
                        self.clicked = True
                    if event.type == pygame.MOUSEBUTTONUP and self.clicked == True:
                        self.clicked = False
                        self.pos = pygame.mouse.get_pos()
                        cell_x = self.pos[0]
                        cell_y = self.pos[1]
                        if self.board[math.floor(cell_x / (self.width / self.GRID_SIZE))][math.floor(cell_y / (self.height / self.GRID_SIZE))] == 0:
                            self.move([math.floor(cell_x / (self.width / self.GRID_SIZE))] + [math.floor(cell_y / (self.height / self.GRID_SIZE))])
                            if not self.mode == "human" and not self.is_game_over():
                                self.play_ai()
                                print("issue1?")
                        
                if not self.is_game_over() and self.ShowMenu:

                    if event.type == pygame.MOUSEBUTTONDOWN and self.clicked == False:
                        self.clicked = True
                    if event.type == pygame.MOUSEBUTTONUP and self.clicked == True:
                        self.clicked = False
                        self.pos = pygame.mouse.get_pos()
                        if self.button1.collidepoint(self.pos):
                            # X or O
                            if (self.player == 1):
                                self.player = -1
                            else:
                                self.player = 1
                            print("Change Setting(player): ", self.player)
                            self.draw_menu()
                        if self.button2.collidepoint(self.pos):
                            # Human or AI
                            if (self.mode == "minimax"):
                                self.mode = "negamax"
                            elif (self.mode == "negamax"):
                                self.mode = "human"
                            elif (self.mode == "human"):
                                self.mode = "minimax"
                            print("Change Setting(mode): ", self.mode)
                            self.draw_menu()
                        if self.button3.collidepoint(self.pos):
                            # Board Size
                            if self.GRID_SIZE == 4:
                                self.GRID_SIZE = 5
                            elif self.GRID_SIZE == 5:
                                self.GRID_SIZE = 6
                            elif self.GRID_SIZE == 6:
                                self.GRID_SIZE = 4
                            print("Change Setting(gridSize): ", self.GRID_SIZE)
                            self.draw_menu()
                        if self.button4.collidepoint(self.pos):
                            # Start game
                            self.ShowMenu = False
                            self.game_reset()
                            print("Start")
                            if (self.mode == "minimax" and self.player == -1 or self.mode == "negamax" and self.player == -1):
                                self.play_ai()
                                print("issue2?")
                                print("player: ", self.player)
                
            clock.tick(60)
            # Update the screen with what was drawn.
            pygame.display.update()

        pygame.quit()

#Start Game
tictactoegame = RandomBoardTicTacToe()
tictactoegame.play_game()
