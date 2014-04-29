"""
checkers_refactored_2.py

A simple (incomplete) checkers engine written in pygame.

Everest Witman - 2014
"""

import pygame, sys
from pygame.locals import *

##COLORS##
#             R    G    B
WHITE    = (255, 255, 255)
BLUE     = (  0,   0, 255)
RED      = (255,   0,   0)
BLACK    = (  0,   0,   0)

class Game:
	"""The main game control."""

	def __init__(self):
		self.graphics = Graphics()
		self.board = Board()

	def setup(self):
		"""Draws the window and board at the beginning of the game"""
		self.graphics.setup_window()
		print self.board.legal_moves((1,5))

	def event_loop(self):
		"""The event loop. This is where events are triggered 
		(like a mouse click) and then effect the game state."""

		for event in pygame.event.get():

			if event.type == QUIT:
				self.terminate_game()

	def update(self):
		"""Calls on the graphics class to update the game display."""
		self.graphics.update_display(self.board.matrix)

	def terminate_game(self):
		"""Quits the program and ends the game."""
		pygame.quit()
		sys.exit

	def main(self):
		""""This executes the game and controls its flow."""
		self.setup()

		while True:
			self.event_loop()
			self.update()

class Graphics:
	def __init__(self):
		self.caption = "Checkers"

		self.fps = 60
		self.clock = pygame.time.Clock()

		self.window_size = 600
		self.screen = pygame.display.set_mode((self.window_size, self.window_size)) 
		self.background = pygame.image.load('resources/board.png')

		self.square_size = self.window_size / 8
		self.piece_size = self.square_size / 2

	def setup_window(self):
		pygame.init()
		pygame.display.set_caption(self.caption)
	
	def update_display(self, board):
		#self.screen.blit(self.background, (0,0))
		self.draw_board_squares(board)
		self.draw_board_pieces(board)

		pygame.display.update()
		self.clock.tick(self.fps)

	def draw_board_squares(self, board):
		"""Take a board object and draws all of its squares to the display"""
		for x in xrange(8):
			for y in xrange(8):
				pygame.draw.rect(self.screen, board[x][y].color, (x * self.square_size, y * self.square_size, self.square_size, self.square_size), )
	
	def draw_board_pieces(self, board):
		"""Take a board object and draws all of its pieces to the display"""
		for x in xrange(8):
			for y in xrange(8):
				if board[x][y].occupant != None:
					pygame.draw.circle(self.screen, board[x][y].occupant.color, self.pixel_coords((x,y)), 600 / 16) 

	def pixel_coords(self, board_coords):
		"""
		Takes in a tuple of board coordinates (x,y) 
		and returns the pixel coordinates of the center of the square at that location.
		"""
		return (board_coords[0] * self.square_size + self.piece_size, board_coords[1] * self.square_size + self.piece_size)


class Board():
	def __init__(self):
		self.matrix = self.new_board()
		self.board_string = self.board_string(self.matrix)
		print self.board_string

	def new_board(self):
		"""Create a new board matrix."""

		# initialize squares and place them in matrix
		matrix = [[None] * 8] * 8

		for x in xrange(8):
			for y in xrange(8):
				if (x % 2 != 0) and (y % 2 == 0):
					matrix[y][x] = Square(WHITE)
				elif (x % 2 != 0) and (y % 2 != 0):
					matrix[y][x] = Square(BLACK)
				elif (x % 2 == 0) and (y % 2 != 0):
					matrix[y][x] = Square(WHITE)
				elif (x % 2 == 0) and (y % 2 == 0): 
					matrix[y][x] = Square(BLACK)

		"""for y in xrange(8):
			for x in xrange(8):
				if y % 2 == 0:
					matrix[y][x] = Square(BLACK)
				else:
					matrix[y][x] = Square(BLUE)

		for y in xrange(1,8,2):
			for x in xrange(8):
				if x % 2 == 0:
					matrix[y][x] = Square(WHITE)
				else:
					matrix[y][x] = Square(BLACK)"""

		"""matrix[0][0] = Square(BLACK)
		matrix[0][1] = Square(WHITE)
		matrix[0][2] = Square(BLACK)
		matrix[0][3] = Square(WHITE)
		matrix[0][4] = Square(BLACK)
		matrix[0][5] = Square(WHITE)
		matrix[0][6] = Square(BLACK)
		matrix[0][7] = Square(WHITE)

		matrix[1][0] = Square(WHITE)
		matrix[1][1] = Square(BLACK)
		matrix[1][2] = Square(WHITE)
		matrix[1][3] = Square(BLACK)
		matrix[1][4] = Square(WHITE)
		matrix[1][5] = Square(BLACK)
		matrix[1][6] = Square(WHITE)
		matrix[1][7] = Square(BLACK)
		
		matrix[2][1] = Square(BLACK)
		matrix[2][2] = Square(WHITE)
		matrix[2][3] = Square(BLACK)
		matrix[2][4] = Square(WHITE)
		matrix[2][5] = Square(BLACK)
		matrix[2][6] = Square(WHITE)
		matrix[2][7] = Square(BLACK)
		
		matrix[3][0] = Square(WHITE)
		matrix[3][1] = Square(BLACK)
		matrix[3][2] = Square(WHITE)
		matrix[3][3] = Square(BLACK)
		matrix[3][4] = Square(WHITE)
		matrix[3][5] = Square(BLACK)
		matrix[3][6] = Square(WHITE)
		matrix[3][7] = Square(BLACK)
		
		matrix[4][0] = Square(BLACK)
		matrix[4][1] = Square(WHITE)
		matrix[4][2] = Square(BLACK)
		matrix[4][3] = Square(WHITE)
		matrix[4][4] = Square(BLACK)
		matrix[4][5] = Square(WHITE)
		matrix[4][6] = Square(BLACK)
		matrix[4][7] = Square(WHITE)

		matrix[5][0] = Square(WHITE)
		matrix[5][1] = Square(BLACK)
		matrix[5][2] = Square(WHITE)
		matrix[5][3] = Square(BLACK)
		matrix[5][4] = Square(WHITE)
		matrix[5][5] = Square(BLACK)
		matrix[5][6] = Square(WHITE)
		matrix[5][7] = Square(BLACK)

		matrix[6][0] = Square(BLACK)
		matrix[6][1] = Square(WHITE)
		matrix[6][2] = Square(BLACK)
		matrix[6][3] = Square(WHITE)
		matrix[6][4] = Square(BLACK)
		matrix[6][5] = Square(WHITE)
		matrix[6][6] = Square(BLACK)
		matrix[6][7] = Square(WHITE)

		matrix[7][0] = Square(WHITE)
		matrix[7][1] = Square(BLACK)
		matrix[7][2] = Square(WHITE)
		matrix[7][3] = Square(BLACK)
		matrix[7][4] = Square(WHITE)
		matrix[7][5] = Square(BLACK)
		matrix[7][6] = Square(WHITE)
		matrix[7][7] = Square(BLACK)"""

		# initialize the pieces and put them in the appropriate squares

		for x in xrange(8):
			for y in xrange(3):
				if matrix[x][y].color == BLACK:
					matrix[x][y].occupant = Piece(RED)
			for y in xrange(5, 8):
				if matrix[x][y].color == BLACK:
					matrix[x][y].occupant = Piece(BLUE)


		return matrix

	def board_string(self, board):
		"""Takes a board and returns a matrix of the board space colors."""

		board_string = [[None] * 8] * 8 

		for x in xrange(8):
			for y in xrange(8):
				if board[x][y].color == WHITE:
					board_string[x][y] = "WHITE"
				else:
					board_string[x][y] = "BLACK"


		return board_string

	def legal_moves(self, coords):
		"""Returns a list of legal moves from a set of coordinates (x,y) on the board."""
		if self.matrix[coords[0]][coords[1]].occupant != None:
			if self.matrix[coords[0]][coords[1]].occupant.color == BLUE:
				if self.matrix[coords[0]][coords[1]].occupant.king == False:
					blind_legal_moves = [(coords[0] - 1, coords[1] - 1), (coords[0] + 1, coords[1] - 1)] # legal moves before considering other pieces
					legal_moves = [] # legal moves considering other pieces

					for move in blind_legal_moves:
						if self.matrix[move[0]][move[1]].occupant == None:
							legal_moves.append(move)

			return legal_moves

		else:
			return []


	def is_end_square(self, coords):
		"""
		Is passed a coordinate tuple (x,y), and returns true or 
		false depending on if that square on the board is an end square.

		===DOCTESTS===

		>>> board = Board()

		>>> board.is_end_square((2,7))
		True

		>>> board.is_end_square((5,0))
		True

		>>>board.is_end_square((0,5))
		False
		"""

		if coords[1] == 0 or coords[1] == 7:
			return True
		else:
			return False

class Piece:
	def __init__(self, color, king = False):
		self.color = color
		self.king = king

class Square:
	def __init__(self, color, occupant = None):
		self.color = color # color is either BLACK or WHITE
		self.occupant = occupant # occupant is a Square object

def main():
	game = Game()
	game.main()

main()

if True:
	if __name__ == "__main__":
		import doctest
		doctest.testmod()

