"""
checker.py

A very simple Checkers engine written with Pygame.

Referenced atari_eric's example of how to drag and drop objects in Pygame 
from http://boards.openpandora.org/topic/11593-drag-and-drop-in-pygame/

Everest Witman - 4 / 2014 - Marlboro College - Programming Workshop
"""


import pygame, sys
from pygame.locals import *

##CONSTANTS##
FPS = 60 # frames per second to update the screen
WINDOW_WIDTH = 800 # width of the program's window in pixels
WINDOW_HEIGHT = 800 # height in pixels
BOARD_SIZE = WINDOW_HEIGHT # width and height of each space on the board in pixels
SPACE_SIZE = BOARD_SIZE / 8 
PIECE_SIZE = SPACE_SIZE / 2 # radius of pieces in pixels

##COLORS##
#             R    G    B
GREY     = (100, 100, 100)
WHITE    = (255, 255, 255)
BLUE     = (  0,   0, 255)
RED      = (255,   0,   0)
BLACK    = (  0,   0,   0)

class Square: # board square 
    def __init__(self, color, pos, size = SPACE_SIZE, end_square = False, movable = True):
        self.color = color
        self.pos = pos # pixel coordinates of upper left corner
        self.size = size
        self.end_square = end_square
        self.movable = False

    def render(self, screen):
        pygame.draw.rect(screen, self.color, (self.pos[0], self.pos[1], self.size, self.size))

class Piece: # game pieces
    def __init__(self, color, pos, size = PIECE_SIZE, movable = True): # initialze the properties of the object
        self.color = color
        self.pos = pos
        self.movable = movable
        self.size = size

    def render(self,screen):
        pygame.draw.circle(screen,self.color,self.pos, self.size)



def draw_board():
    """
    Draws the Checkers board.
    """

    color_counter = 0

    x_counter = 0
    y_counter = 0


    while y_counter < BOARD_SIZE:
        color_counter = 1
        x_counter = 0

        while x_counter < BOARD_SIZE:
            if color_counter % 2 == 0:
                color = WHITE
            else:
                color = BLACK 
            
            square = Square(color, (x_counter, y_counter))
            square.render(screen)

            color_counter += 1
            x_counter += SPACE_SIZE

        y_counter += SPACE_SIZE * 2


    y_counter = SPACE_SIZE

    while y_counter < BOARD_SIZE:
        color_counter = 0
        x_counter = 0

        while x_counter < BOARD_SIZE:
            if color_counter % 2 == 0:
                color = WHITE
            else:
                color = BLACK 
            
            square = Square(color, (x_counter, y_counter))
            square.render(screen)

            color_counter += 1
            x_counter += SPACE_SIZE

        y_counter += SPACE_SIZE * 2

        pass

def setup_pieces():
    """
    Sets up the pieces at the start of the game.
    """

    row_counter = 1

    x_counter = int(SPACE_SIZE * 0.5)
    y_counter = int(SPACE_SIZE * 0.5)

    color = RED
    while y_counter < SPACE_SIZE * 3.5:

        if row_counter % 2 == 0:
            x_counter = int(SPACE_SIZE * 1.5)
        else:
            x_counter = int(SPACE_SIZE * 0.5)

        while x_counter < BOARD_SIZE:

            piece = Piece(color, (x_counter, y_counter))
            render_list.append(piece)

            x_counter += SPACE_SIZE * 2

        y_counter += SPACE_SIZE
        row_counter += 1


    row_counter = 8

    x_counter = int(SPACE_SIZE * 0.5)
    y_counter = int(BOARD_SIZE - (SPACE_SIZE * 0.5))

    color = BLUE
    while y_counter > BOARD_SIZE - (SPACE_SIZE * 3.5):

        if row_counter % 2 == 0:
            x_counter = int(SPACE_SIZE * 1.5)
        else:
            x_counter = int(SPACE_SIZE * 0.5)

        while x_counter < BOARD_SIZE:

            piece = Piece(color, (x_counter, y_counter))
            render_list.append(piece)

            x_counter += SPACE_SIZE * 2

        y_counter -= SPACE_SIZE
        row_counter -= 1

    pass

def terminate():
    # terminates the program
    pygame.quit()
    sys.exit()


def main(): # main game loop
    global FPSCLOCK, screen, render_list

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Checkers")

    render_list = [] # list of objects
    mouse_pressed = False # Pressed down THIS FRAME
    mouse_down = False # mouse is held down
    mouse_released = False # Released THIS FRAME
    target = None # target of Drag/Drop

    setup_pieces()

    while True: # main game loop
        draw_board() # clear screen

        mouse_pos = pygame.mouse.get_pos()
        
        for Event in pygame.event.get():
            if Event.type == pygame.QUIT:
                terminate()
            
            if Event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True 
                mouse_down = True 
               
            if Event.type == pygame.MOUSEBUTTONUP:
                mouse_released = True
                mouse_down = False
             
        if mouse_pressed == True:
            for item in render_list: # search all items
                if (mouse_pos[0] >= (item.pos[0]-item.size) and 
                    mouse_pos[0] <= (item.pos[0]+item.size) and 
                    mouse_pos[1] >= (item.pos[1]-item.size) and 
                    mouse_pos[1] <= (item.pos[1]+item.size) and
                    item.movable == True): # inside the bounding box
                    target = item # "pick up" item
            
        if mouse_down and target is not None: # if we are dragging something
            target.pos = mouse_pos # move the target with us
        
        if mouse_released:
            target = None # Drop item, if we have any
            
        for item in render_list:
            item.render(screen) # Draw all items
            
        mouse_pressed = False # Reset these to False
        mouse_released = False 

        pygame.display.update()
        FPSCLOCK.tick(FPS)

    pass # End of function

if __name__ == '__main__': # Are we RUNNING from this module?
    main() # Execute our main function