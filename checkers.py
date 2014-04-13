"""
checkers.py

Prints a Checkers board to the screen.

Everest Witman - 2014 - Marlboro College - Programming Workshop
"""

import pygame, sys
from pygame.locals import *

##CONSTANTS##
FPS = 60 # frames per second to update the screen
WINDOW_WIDTH = 800 # width of the program's window in pixels
WINDOW_HEIGHT = 800 # height in pixels
BOARD_SIZE = 700 # width and height of each space on the board in pixels
SPACE_SIZE = BOARD_SIZE / 8 


# Amount of space on the left & right side (XMARGIN) or above and below
# (YMARGIN) the game board, in pixels.
XMARGIN = int((WINDOW_WIDTH - BOARD_SIZE) / 2)
YMARGIN = int((WINDOW_HEIGHT - BOARD_SIZE) / 2)

##COLORS##

#             R    G    B
GRAY     = (100, 100, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
BLACK    = (  0,   0,   0)

def main():
	global FPSCLOCK, DISPLAYSURF

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption("Checkers")

	# set up the background image
	board_image = pygame.image.load("resources/board.png")
	board_image = pygame.transform.smoothscale(board_image, (BOARD_SIZE, BOARD_SIZE))

	while True: # main game loop
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
		
		DISPLAYSURF.blit(board_image,(XMARGIN,YMARGIN))

		pygame.display.update()
		FPSCLOCK.tick(FPS)

def terminate():
	# terminates the program
	pygame.quit()
	sys.exit()

main()