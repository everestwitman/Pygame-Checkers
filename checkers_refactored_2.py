"""
checkers_refactored_2.py

A simple (incomplete) checkers engine written in Python with the pygame 1.9.2 libraries.

Here are the rules I am using: http://boardgames.about.com/cs/checkersdraughts/ht/play_checkers.htm

I adapted some code from checkers.py found at http://boardgames.about.com/cs/checkersdraughts/ht/play_checkers.htm/checkers.py starting on line 159 of my program.

=== TO DO ==
Capturing 
Higlight Legal Move's
Kinging
Check for Endgame

Everest Witman - May 2014 - Marlboro College - Programming Workshop 
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
		
		self.turn = BLUE
		self.selected_piece = None # a board location. 

	def setup(self):
		"""Draws the window and board at the beginning of the game"""
		self.graphics.setup_window()

	def event_loop(self):
		"""
		The event loop. This is where events are triggered 
		(like a mouse click) and then effect the game state.
		"""
		self.mouse_pos = self.graphics.board_coords(pygame.mouse.get_pos()) # what square is the mouse in?

		for event in pygame.event.get():

			if event.type == QUIT:
				self.terminate_game()

			if event.type == MOUSEBUTTONDOWN:
		
				if self.board.location(self.mouse_pos).occupant != None and self.board.location(self.mouse_pos).occupant.color == self.turn:
					self.selected_piece = self.mouse_pos

				elif self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece):

					self.board.move_piece(self.selected_piece, self.mouse_pos)

					self.end_turn()
					self.selected_piece = None

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

		while True: # main game loop
			self.event_loop()
			self.update()

	def end_turn(self):
		"""
		End the turn. Switches the current player. 
		"""
		if self.turn == BLUE:
			self.turn = RED
		else:
			self.turn = BLUE

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
		self.screen.blit(self.background, (0,0))
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

	def board_coords(self, (pixel_x, pixel_y)):
		return (pixel_x / self.square_size, pixel_y / self.square_size)		

class Board():
	def __init__(self):
		self.matrix = self.new_board()

	def new_board(self):
		"""Create a new board matrix."""

		# initialize squares and place them in matrix

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

	def adjacent(self, (x,y)):
		"""
		Returns a list of squares locations that are adjacent (on a diagonal) to (x,y).
		"""

		return [self.rel(NORTHWEST, (x,y)), self.rel(NORTHEAST, (x,y)),self.rel(SOUTHWEST, (x,y)),self.rel(SOUTHEAST, (x,y))]

	def location(self, (x,y)):
		"""
		Takes a set of coordinates as arguments and returns self.matrix[x][y]
		"""
		return self.matrix[x][y]

	def blind_legal_moves(self, (x,y)):
		"""
		Returns a list of blind legal move locations from a set of coordinates (x,y) on the board. 
		If that location is empty, then blind_legal_moves() return an empty list.
		"""

		if self.matrix[x][y].occupant != None:
			
			if self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == BLUE:
				blind_legal_moves = [self.rel(NORTHWEST, (x,y)), self.rel(NORTHEAST, (x,y))]
				
			elif self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == RED:
				blind_legal_moves = [self.rel(SOUTHWEST, (x,y)), self.rel(SOUTHEAST, (x,y))]

			else:
				blind_legal_moves = [self.rel(NORTHWEST, (x,y)), self.rel(NORTHEAST, (x,y)), self.rel(SOUTHWEST, (x,y)), self.rel(SOUTHEAST, (x,y))]

		else:
			blind_legal_moves = []

		return blind_legal_moves

	def legal_moves(self, (x,y)):
		"""
		Returns a list of legal move locations from a given set of coordinates (x,y) on the board.
		If that location is empty, then legal_moves() returns an empty list.
		"""

		blind_legal_moves = self.blind_legal_moves((x,y)) 
		legal_moves = []

		for move in blind_legal_moves:

			if self.on_board(move):

				if self.location(move).occupant == None:
					legal_moves.append(move)

				elif self.location(move).occupant.color != self.location((x,y)).occupant.color and self.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant == None: # is this location filled by an enemy piece?
					legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

		return legal_moves

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

	def on_board(self, (x,y)):
		"""
		Checks to see if the given square (x,y) lies on the board.
		If it does, then on_board() return True. Otherwise it returns false.

		===DOCTESTS===
		>>> board = Board()

		>>> board.on_board((5,0)):
		True

		>>> board.on_board(-2, 0):
		False

		>>> board.on_board(3, 9):
		False
		"""

		if x < 0 or y < 0 or x > 7 or y > 7:
			return False
		else:
			return True


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

