"""
checkers_refactored_2.py

A simple (incomplete) checkers engine written in pygame. 

Here are the rules I am using: http://boardgames.about.com/cs/checkersdraughts/ht/play_checkers.htm

I adapt some code from checkers.py on line 130 found at http://boardgames.about.com/cs/checkersdraughts/ht/play_checkers.htm 

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

##DIRECTIONS##
NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"

class Game:
	"""The main game control."""

	def __init__(self):
		self.graphics = Graphics()
		self.board = Board()

	def setup(self):
		"""Draws the window and board at the beginning of the game"""
		self.graphics.setup_window()

		self.board.move_piece((1,5),(self.board.legal_moves((1,5))[0]))
		print self.board.legal_moves((0,4))

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

		matrix =[[None, None, None, None, None, None, None, None],
				 [None, None, None, None, None, None, None, None],
				 [None, None, None, None, None, None, None, None],
				 [None, None, None, None, None, None, None, None],
				 [None, None, None, None, None, None, None, None],
				 [None, None, None, None, None, None, None, None],
				 [None, None, None, None, None, None, None, None],
				 [None, None, None, None, None, None, None, None]]

		matrix = [[None] * 8 for i in xrange(8)]

		# The following code block has been adapted from http://itgirl.dreamhosters.com/itgirlgames/games/Program%20Leaders/ClareR/Checkers/checkers.py
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
	
	def rel(self, dir, (x,y)):
		if dir == NORTHWEST:
			return (x - 1, y - 1)
		elif dir == NORTHEAST:
			return (x + 1, y - 1)
		elif dir == SOUTHWEST:
			return (x - 1, y + 1)
		elif dir == SOUTHEAST:
			return (x + 1, y + 1)
		else:
			return 0

	def legal_moves(self, (x,y)):
		"""Returns a list of legal move locations from a set of coordinates (x,y) on the board."""
		if self.matrix[x][y].occupant != None:
			if self.matrix[x][y].occupant.color == BLUE:
				if self.matrix[x][y].occupant.king == False:
					blind_legal_moves = [self.rel(NORTHWEST, (x,y)), self.rel(NORTHEAST, (x,y))] # legal moves before considering other pieces
				else: 
					blind_legal_moves = [self.rel(NORTHWEST, (x,y)), self.rel(NORTHEAST, (x,y)), self.rel(SOUTHWEST, (x,y)), self.rel(SOUTHEAST, (x,y))]

		legal_moves = [] # legal moves considering other pieces

		for move in blind_legal_moves:
			if self.matrix[move[0]][move[1]].occupant == None and move[0] >= 0 and move[1] >= 0:
				legal_moves.append(move)


			return legal_moves

		else:
			return []

	def remove_piece(self, (x,y)):
		"""Removes a piece from the board at position (x,y). """
		self.matrix[x][y].occupant = None

	def move_piece(self, (start_x, start_y), (end_x, end_y)):
		"""Move a piece from (start_x, start_y) to (end_x, end_y)."""

		self.matrix[end_x][end_y].occupant = self.matrix[start_x][start_y].occupant
		self.remove_piece((start_x, start_y))


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

DOCTEST = False

if DOCTEST:
	if __name__ == "__main__":
		import doctest
		doctest.testmod()

