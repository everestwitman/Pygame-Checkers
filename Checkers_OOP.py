"""
checkers_OOP.py

A very simple Checkers engine written with Pygame.

Everest Witman - 4 / 2014 - Marlboro College - Programming Workshop
"""

import pygame, sys, math
from pygame.locals import *

##COLORS##
#             R    G    B
WHITE    = (255, 255, 255)
BLUE     = (  0,   0, 255)
RED      = (255,   0,   0)
BLACK    = (  0,   0,   0)

class Game:
    def __init__(self, turn = BLUE):
        self.turn = turn # who's turn is it?
        self.board = Board()
        self.graphics = Graphics()

    def setup(self):
        self.graphics.setup_window()

    def event_loop(self):
        mouse_pos = pygame.mouse.get_pos()
        square_to_move = None
        piece_moved = False
        self.mouse_pressed = False

        for event in pygame.event.get():

            if event.type == QUIT:
                self.terminate()

            if event.type == MOUSEBUTTONDOWN and self.board.board_matrix[self.graphics.mouse_in_square(mouse_pos)[1]][self.graphics.mouse_in_square(mouse_pos)[0]] != None and self.board.board_matrix[self.graphics.mouse_in_square(mouse_pos)[1]][self.graphics.mouse_in_square(mouse_pos)[0]].occupent != None:
                if self.board.board_matrix[self.graphics.mouse_in_square(mouse_pos)[1]][self.graphics.mouse_in_square(mouse_pos)[0]].occupent.color == self.turn:
                    square_to_move = self.graphics.mouse_in_square(mouse_pos)

                    while piece_moved == False:
                        mouse_pos = pygame.mouse.get_pos()

                        for Event in pygame.event.get():
                            if Event.type == MOUSEBUTTONDOWN and self.board.board_matrix[self.graphics.mouse_in_square(mouse_pos)[1]][self.graphics.mouse_in_square(mouse_pos)[0]] != None and self.board.board_matrix[self.graphics.mouse_in_square(mouse_pos)[1]][self.graphics.mouse_in_square(mouse_pos)[0]].occupent == None:
                                self.board.move_piece(square_to_move, self.graphics.mouse_in_square(mouse_pos))
                                piece_moved = True
                                self.new_turn()


    def update(self,):
        # update both the GUI and game state
        self.graphics.update_display(self.board.board_matrix)

    def terminate(self):
        pygame.quit()
        sys.exit()

    def main(self): # main game loop
        self.setup()

        while True:
            self.event_loop()
            self.update()

    def new_turn(self):
        """Switches who's turn it is."""

        if self.turn == BLUE:
            self.turn = RED
        else:
            self.turn = BLUE

        
class Board:
    def __init__(self):
        self.board_matrix = self.new_board()

    def new_board(self):
        # initialize pieces

        """self.pieces = [None] * 24
        for i in range(12):
            self.pieces[i] = Piece[RED]
        for i in range(13, 24):
            self.pieces[i] = Piece[BLUE]"""

        piece_red_1 = Piece(RED)
        piece_red_2 = Piece(RED)
        piece_red_3 = Piece(RED)
        piece_red_4 = Piece(RED)
        piece_red_5 = Piece(RED)
        piece_red_6 = Piece(RED)
        piece_red_7 = Piece(RED)
        piece_red_8 = Piece(RED)
        piece_red_9 = Piece(RED)
        piece_red_10 = Piece(RED)
        piece_red_11 = Piece(RED)
        piece_red_12 = Piece(RED)

        piece_blue_1 = Piece(BLUE)
        piece_blue_2 = Piece(BLUE)
        piece_blue_3 = Piece(BLUE)
        piece_blue_4 = Piece(BLUE)
        piece_blue_5 = Piece(BLUE)
        piece_blue_6 = Piece(BLUE)
        piece_blue_7 = Piece(BLUE)
        piece_blue_8 = Piece(BLUE)
        piece_blue_9 = Piece(BLUE)
        piece_blue_10 = Piece(BLUE)
        piece_blue_11 = Piece(BLUE)
        piece_blue_12 = Piece(BLUE)

        # initialize squares
        square_1 = Square(piece_red_1, True)
        square_2 = Square(piece_red_2, True)
        square_3 = Square(piece_red_3, True)
        square_4 = Square(piece_red_4, True)
        square_5 = Square(piece_red_5)
        square_6 = Square(piece_red_6)
        square_7 = Square(piece_red_7)
        square_8 = Square(piece_red_8)
        square_9 = Square(piece_red_9)
        square_10 = Square(piece_red_10)
        square_11 = Square(piece_red_11)
        square_12 = Square(piece_red_12)

        square_13 = Square()
        square_14 = Square()
        square_15 = Square()
        square_16 = Square()
        square_17 = Square()
        square_18 = Square()
        square_19 = Square()
        square_20 = Square()

        square_21 = Square(piece_blue_1)
        square_22 = Square(piece_blue_2)
        square_23 = Square(piece_blue_3)
        square_24 = Square(piece_blue_4)
        square_25 = Square(piece_blue_5)
        square_26 = Square(piece_blue_6)
        square_27 = Square(piece_blue_7)
        square_28 = Square(piece_blue_8)
        square_29 = Square(piece_blue_9, True)
        square_30 = Square(piece_blue_10, True)
        square_31 = Square(piece_blue_11, True)
        square_32 = Square(piece_blue_12, True)

        # board matrix 
        # indices ( board[y][x] )of each element corrospond to their coordinates on the board
        board = [[square_1, None, square_2, None, square_3, None, square_4, None],
                [None, square_5, None, square_6, None, square_7, None, square_8],
                [square_9, None, square_10, None, square_11, None, square_12, None],
                [None, square_13, None, square_14, None, square_15, None, square_16],
                [square_17, None, square_18, None, square_19, None, square_20, None],
                [None,square_21, None, square_22, None, square_23, None, square_24],
                [square_25, None, square_26, None, square_27, None, square_28, None],
                [None, square_29, None, square_30, None, square_31, None, square_32]]

        return board

    def move_piece(self, start_coords, end_coords):
        # both are arguments are (x,y)
        self.board_matrix[end_coords[1]][end_coords[0]].occupent = self.board_matrix[start_coords[1]][start_coords[0]].occupent
        self.board_matrix[start_coords[1]][start_coords[0]].occupent = None

    def capture_piece(self, coords):
        self.board_matrix[coords[1]][coords[0]].occupent = None

class Graphics:
    def __init__(self, caption = "Checkers", fps = 60, window_size = 600, background = pygame.image.load('resources/board.png')):
        # pixel diameter of pieces and have board squares
        self.piece_size = 75

        self.caption = caption # displayed at the top of the window

        self.fps = fps # frames per second
        self.clock = pygame.time.Clock()

        self.window_size = window_size
        self.screen = pygame.display.set_mode((window_size, window_size))
        self.background = background
        self.mouse_pos = (0,0)

    def setup_window(self):
        pygame.init()
        pygame.display.set_caption(self.caption)

        self.screen.blit(self.background, (0,0))
        self.clock.tick(self.fps)

    def update_display(self, board):
        self.mouse_pos = pygame.mouse.get_pos()

        self.screen.blit(self.background, (0,0))
        self.draw_board(board)
        pygame.display.update()


    def draw_piece(self, square, board_coords, color):
        coords = (int((board_coords[0]) * self.piece_size + self.piece_size / 2),int((board_coords[1]) * self.piece_size + self.piece_size / 2))

        pygame.draw.circle(self.screen, color, coords, self.piece_size / 2)

    def draw_board(self, board):
        for x in xrange(0,8):
            for y in xrange(0,8):
                if (board[y][x] != None and board[y][x].occupent != None):
                    self.draw_piece(board[y][x], (x,y), board[y][x].occupent.color)

    def mouse_in_square(self, mouse_pos):
        """Returns the board position as (x,y). Takes the pixel position of the mouse as an imput."""
        board_coords = ((mouse_pos[0] / self.piece_size), (mouse_pos[1] / self.piece_size))    
        return board_coords

class Square:
    def __init__(self, occupent = None, end_square = False):
        self.occupent = occupent # a Piece object
        self.end_square = end_square # is it an end square?

class Piece:
    def __init__(self, color, king = False):
        self.color = color
        self.king = king # is it a king?

def main():
    game = Game()

    game.main()

main()