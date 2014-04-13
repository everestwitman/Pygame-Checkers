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
BOARD_SIZE = WINDOW_HEIGHT # width and height of each space on the board in pixels
SPACE_SIZE = BOARD_SIZE / 8 
PIECE_SIZE = SPACE_SIZE / 2 # radius of pieces in pizels

##COLORS##

#             R    G    B
GRAY     = (100, 100, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
BLACK    = (  0,   0,   0)
WHITE2   = (230, 230, 230)

def main():
	global FPSCLOCK, DISPLAYSURF

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption("Checkers")

	draw_board()
	setup_pieces()

	while True: # main game loop
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()

		pygame.display.update()
		FPSCLOCK.tick(FPS)

def terminate():
	# terminates the program
	pygame.quit()
	sys.exit()

def draw_board():
	"""
	Draws the Checkers board.
	"""
	pygame.draw.rect(DISPLAYSURF, WHITE, (0,0, BOARD_SIZE, BOARD_SIZE))
	
	spacex = 0
	spacey = 0

	while spacex < BOARD_SIZE:
		spacey = 0
		while spacey < BOARD_SIZE:
			pygame.draw.rect(DISPLAYSURF, BLACK, (spacex, spacey, SPACE_SIZE, SPACE_SIZE))
			spacey += SPACE_SIZE * 2
		spacex += SPACE_SIZE * 2

	spacex = SPACE_SIZE
	while spacex < BOARD_SIZE:
		spacey = SPACE_SIZE
		while spacey < BOARD_SIZE:
			pygame.draw.rect(DISPLAYSURF, BLACK, (spacex, spacey, SPACE_SIZE, SPACE_SIZE))
			spacey += SPACE_SIZE * 2
		spacex += SPACE_SIZE * 2

	pass

def setup_pieces():
	"""
	Sets up the pieces.
	"""

	# set up red pieces
	spacex = int(SPACE_SIZE * 0.5)
	spacey = int(SPACE_SIZE * 0.5)

	while spacex < BOARD_SIZE:
			pygame.draw.circle(DISPLAYSURF, RED, (spacex, spacey), PIECE_SIZE, 0)
			spacex += SPACE_SIZE * 2

	spacex = int(SPACE_SIZE * 1.5)
	spacey = int(SPACE_SIZE * 1.5)

	while spacex < BOARD_SIZE:
			pygame.draw.circle(DISPLAYSURF, RED, (spacex, spacey), PIECE_SIZE, 0)
			spacex += SPACE_SIZE * 2


	# setup white pieces
	spacex = int(SPACE_SIZE * 0.5)
	spacey = int(BOARD_SIZE - (SPACE_SIZE * 1.5))
	while spacex < BOARD_SIZE:
			pygame.draw.circle(DISPLAYSURF, WHITE2, (spacex, spacey), PIECE_SIZE, 0)
			spacex += SPACE_SIZE * 2

	spacex = int(SPACE_SIZE * 1.5)
	spacey = int(BOARD_SIZE - (SPACE_SIZE * 0.5))

	while spacex < BOARD_SIZE:
			pygame.draw.circle(DISPLAYSURF, WHITE2, (spacex, spacey), PIECE_SIZE, 0)
			spacex += SPACE_SIZE * 2


	pass

main()