import copy
import pygame, sys
from pygame.locals import *
import numpy as np

pygame.font.init()

##COLORS##
#             R    G    B 
WHITE    = (255, 255, 255)
BLUE     = (  0,  70, 255)
RED      = (255,  65, 255)
BLACK    = (  0,   0,   0)
GOLD     = (255, 215,   0)
HIGH     = (160, 190, 255)

##DIRECTIONS##
NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"

"""

Edits throughout the code:
	Changed tuple syntax to work with python 3
	Added must-capture rule
	Added alpha-beta game play AI agent adapted from AIMA code https://github.com/aimacode

Author: William Ament
"""

class Agent:
	def __init__(self, game, state):
		self.game = game
		self.state = state

	def alpha_beta_cutoff_search(self, state, game, d=4, cutoff_test=None, eval_fn=None):
		"""Search game to determine best action; use alpha-beta pruning.
    	This version cuts off search and uses an evaluation function."""
		
		player = game.to_move()

    	# Functions used by alpha_beta
		def max_value(state, alpha, beta, depth):
			if cutoff_test(depth):
				return eval_fn(state)
			v = -np.inf
			for a in game.actions(state):
				v = max(v, min_value(game.result(state, a), alpha, beta, depth + 1))
				if v >= beta:
					return v
				alpha = max(alpha, v)
			return v
		def min_value(state, alpha, beta, depth):
			if cutoff_test(depth):
				return eval_fn(state)
			v = np.inf
			for a in game.actions(state):
				v = min(v, max_value(game.result(state, a), alpha, beta, depth + 1))
				if v <= alpha:
					return v
				beta = min(beta, v)
				return v

    	# Body of alpha_beta_cutoff_search starts here:
    	# The default test cuts off at depth d or at a terminal state
		cutoff_test = (cutoff_test or (lambda depth: depth > d or game.check_for_endgame()))
		eval_fn = eval_fn or (lambda state: game.utility(state, player))
		best_score = -np.inf
		beta = np.inf
		best_action = None
		for a in game.actions(state):
			v = min_value(game.result(state, a), best_score, beta, 1)
			if v > best_score:
				best_score = v
				best_action = a
			return best_action


	def update_state(self, state):
		self.state = state
	
	

	



"""
-----------------ORIGINAL COMMENTS ---------------
checkers.py

A simple checkers engine written in Python with the pygame 1.9.1 libraries.

Here are the rules I am using: http://boardgames.about.com/cs/checkersdraughts/ht/play_checkers.htm

I adapted some code from checkers.py found at 
http://itgirl.dreamhosters.com/itgirlgames/games/Program%20Leaders/ClareR/Checkers/checkers.py starting on line 159 of my program.

This is the final version of my checkers project for Programming Workshop at Marlboro College. The entire thing has been rafactored and made almost completely object oriented.

Funcitonalities include:

- Having the pieces and board drawn to the screen

- The ability to move pieces by clicking on the piece you want to move, then clicking on the square you would
  like to move to. You can change you mind about the piece you would like to move, just click on a new piece of yours.

- Knowledge of what moves are legal. When moving pieces, you'll be limited to legal moves.

- Capturing

- DOUBLE capturing etc.

- Legal move and captive piece highlighting

- Turn changes

- Automatic kinging and the ability for them to move backwords

- Automatic check for and end game. 

- A silky smoooth 60 FPS!

Everest Witman - May 2014 - Marlboro College - Programming Workshop 
"""

class Game:
	"""
	The main game control.
	"""

	def __init__(self):
		self.graphics = Graphics()
		self.board = Board()
		
		self.turn = BLUE
		self.selected_piece = None # a board location. 
		self.peices = self.board.legal_pieces(self.turn) # a list of possible peices to move, used to enforce jumping rules
		self.hop = False
		self.selected_legal_moves = []

		self.agent = Agent(self, self.board)

	def setup(self):
		"""Draws the window and board at the beginning of the game"""
		self.graphics.setup_window()

	def event_loop(self):
		"""
		The event loop. This is where events are triggered 
		(like a mouse click) and then effect the game state.
		"""

		#user plays with this code 
		self.mouse_pos = self.graphics.board_coords(pygame.mouse.get_pos()) # what square is the mouse in?

		#only allow legal moves, restricted by "must-jump" rule
		if self.selected_piece != None and self.selected_piece in self.peices:
			self.selected_legal_moves = self.board.legal_moves(self.selected_piece, self.hop)

		if self.turn == RED:
			self.agent.update_state(self.board)
			move = self.agent.alpha_beta_cutoff_search(self.board, self, 4, None, self.eval2)
			self.board.move_piece(move[0], move[1])

			if move[1] not in self.board.adjacent(move[0]):
				self.hop = True
				self.board.remove_piece((int(move[0][0] + (move[1][0] - move[0][0]) / 2), int(move[0][1] + (move[1][1] - move[0][1]) / 2)))
				if self.board.legal_moves(move[1], self.hop) == []:
					self.end_turn()
					return
			if not self.hop:
				self.end_turn()
				return

		for event in pygame.event.get():

			if event.type == QUIT:
				self.terminate_game()

			if event.type == MOUSEBUTTONDOWN:

				#jumping
				if self.hop == False:
					#ensure the selected piece is in the set of legal peices
					if self.board.location(self.mouse_pos).occupant != None and self.board.location(self.mouse_pos).occupant.color == self.turn:
						self.selected_piece = self.mouse_pos

					elif self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece) and self.selected_piece in self.peices:

						self.board.move_piece(self.selected_piece, self.mouse_pos)
					
						if self.mouse_pos not in self.board.adjacent(self.selected_piece):
							self.board.remove_piece((int(self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) / 2), int(self.selected_piece[1] + (self.mouse_pos[1] - self.selected_piece[1]) / 2)))

							self.hop = True
							self.peices = self.board.legal_pieces(self.turn)
							self.selected_piece = self.mouse_pos

						else:
							self.end_turn()

				#double jumping
				if self.hop == True:

					if self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece, self.hop):
						self.board.move_piece(self.selected_piece, self.mouse_pos)
						self.board.remove_piece((int(self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) / 2), int(self.selected_piece[1] + (self.mouse_pos[1] - self.selected_piece[1]) / 2)))

					if self.board.legal_moves(self.selected_piece, self.hop) == []:
							self.end_turn()


	def update(self):
		"""Calls on the graphics class to update the game display."""
		self.graphics.update_display(self.board, self.selected_legal_moves, self.selected_piece)

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
		end_turn() also checks for end game and resets a lot of class attributes.
		"""
		if self.turn == BLUE:
			self.turn = RED
			print("Blue turn ended")
			self.peices = self.board.legal_pieces(self.turn)
		else:
			self.turn = BLUE
			print("Pink turn ended")
			self.peices = self.board.legal_pieces(self.turn)

		self.selected_piece = None
		self.selected_legal_moves = []
		self.hop = False

		if self.check_for_endgame():
			if self.turn == BLUE:
				self.graphics.draw_message("RED WINS!")
			else:
				self.graphics.draw_message("BLUE WINS!")

	def check_for_endgame(self):
		"""
		Checks to see if a player has run out of moves or pieces. If so, then return True. Else return False.
		"""
		for x in range(8):
			for y in range(8):
				if self.board.location((x,y)).color == BLACK and self.board.location((x,y)).occupant != None and self.board.location((x,y)).occupant.color == self.turn:
					if self.board.legal_moves((x,y)) != []:
						return False

		return True
	
	#added by William Ament
	#returns current turn
	def to_move(self):
		return self.turn
	
	def actions(self, state):
		legal_pieces = state.legal_pieces(self.turn)
		all_legal_moves = []
		for piece in legal_pieces:
			legal_moves = state.legal_moves(piece)
			for move in legal_moves:
				all_legal_moves.append((piece, move))
		return all_legal_moves

	def result(self, state, move):
		if move not in self.actions(state):
			return state

		board = copy.deepcopy(state)
		#adapted from event_loop

		board.move_piece(move[0], move[1])
		if move[1] not in board.adjacent(move[0]):
			board.remove_piece((int(move[0][0] + (move[1][0] - move[0][0]) / 2), int(move[0][1] + (move[1][1] - move[0][1]) / 2)))
		return board 

	def eval(self, state):
		#agent is red
		#count of checkers
		numBlue = 0
		numRed = 0
		numWT = 1.0
		#count of kings
		numBlueKings = 0
		numRedKings = 0
		kingWT = 1.0
		#sum of distance from opposite side
		blueDist = 0
		redDist = 0
		distWT = 1.0
		
		for x in range(8):
			for y in range(8):
				space = state.location((x,y)).occupant
				if space != None and space.color == BLUE:
					if space.king:
						numBlueKings +=1
					numBlue +=1
					blueDist += y
				elif space != None and space.color == RED:
					if space.king:
						numRedKings +=1
					numRed +=1
					redDist += (7-y)

		return numWT*(numRed - numBlue) + kingWT*(numRedKings - numBlueKings) + distWT*(redDist - blueDist)
	
	def eval2(self, state):
		#agent is red
		#count of checkers
		numBlue = 0
		numRed = 0
		numWT = 1.0
		#count of kings
		numBlueKings = 0
		numRedKings = 0
		kingWT = 1.0
		#sum of distance from opposite side
		blueDist = 0
		redDist = 0
		distWT = 1.0
		#count of pieces on the back row
		blueBack = 0
		redBack = 0
		backWT = 1.0
		#count of pieces that are protected from being jumped
		blueProtec = 0
		redProtec = 0
		protecWT = 1.0


		for x in range(8):
			for y in range(8):
				space = state.location((x,y)).occupant
				if space != None and space.color == BLUE:
					if space.king:
						numBlueKings +=1
					numBlue +=1
					blueDist += y
					if y == 7:
						blueBack +=1
						blueProtec +=1
					if y < 7:
						if x == 0 or x == 7:
							blueProtec +=1
						else:
							if (x-1) >= 0 and (x+1) < 8 and (y+1) < 8:
								if (state.location((x-1,y+1)).occupant != None and (state.location((x-1,y+1)).occupant.color == BLUE or state.location((x-1,y+1)).occupant.king)) and (state.location((x+1,y+1)).occupant != None and (state.location((x+1,y+1)).occupant.color == BLUE or state.location((x+1, y+1)).occupant.king)):
									blueProtec +=1

				elif space != None and space.color == RED:
					if space.king:
						numRedKings +=1
					numRed +=1
					redDist += (7-y)
					if y == 0:
						redBack +=1
						redProtec +=1
					if y > 0:
						if x == 0 or x == 7:
							redProtec +=1
						else:
							if (x-1) >= 0 and (x+1) < 8 and (y+1) < 8:
								if (state.location((x-1,y+1)).occupant != None and (state.location((x-1,y+1)).occupant.color == RED or state.location((x-1,y+1)).occupant.king)) and (state.location((x+1,y+1)).occupant != None and (state.location((x+1,y+1)).occupant.color == RED or state.location((x+1, y+1)).occupant.king)):
									redProtec +=1

		return numWT*(numRed - numBlue) + kingWT*(numRedKings - numBlueKings) + distWT*(redDist - blueDist) + backWT*(redBack - blueBack) + protecWT*(redProtec - blueProtec)


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

		self.message = False

	def setup_window(self):
		"""
		This initializes the window and sets the caption at the top.
		"""
		pygame.init()
		pygame.display.set_caption(self.caption)

	def update_display(self, board, legal_moves, selected_piece):
		"""
		This updates the current display.
		"""
		self.screen.blit(self.background, (0,0))
		
		self.highlight_squares(legal_moves, selected_piece)
		self.draw_board_pieces(board)

		if self.message:
			self.screen.blit(self.text_surface_obj, self.text_rect_obj)

		pygame.display.update()
		self.clock.tick(self.fps)

	def draw_board_squares(self, board):
		"""
		Takes a board object and draws all of its squares to the display
		"""
		for x in range(8):
			for y in range(8):
				pygame.draw.rect(self.screen, board[x][y].color, (x * self.square_size, y * self.square_size, self.square_size, self.square_size), )
	
	def draw_board_pieces(self, board):
		"""
		Takes a board object and draws all of its pieces to the display
		"""
		for x in range(8):
			for y in range(8):
				if board.matrix[x][y].occupant != None:
					pygame.draw.circle(self.screen, board.matrix[x][y].occupant.color, self.pixel_coords((x,y)), self.piece_size) 

					if board.location((x,y)).occupant.king == True:
						pygame.draw.circle(self.screen, GOLD, self.pixel_coords((int(x),int(y))), int(self.piece_size / 1.7), int(self.piece_size / 4))


	def pixel_coords(self, board_coords):
		"""
		Takes in a tuple of board coordinates (x,y) 
		and returns the pixel coordinates of the center of the square at that location.
		"""
		return (int(board_coords[0] * self.square_size + self.piece_size), int(board_coords[1] * self.square_size + self.piece_size))

	def board_coords(self, pixel):
		"""
		Does the reverse of pixel_coords(). Takes in a tuple of of pixel coordinates and returns what square they are in.
		"""
		return (int(pixel[0] / self.square_size), int(pixel[1] / self.square_size))

	def highlight_squares(self, squares, origin):
		"""
		Squares is a list of board coordinates. 
		highlight_squares highlights them.
		"""
		for square in squares:
			pygame.draw.rect(self.screen, HIGH, (square[0] * self.square_size, square[1] * self.square_size, self.square_size, self.square_size))	

		if origin != None:
			pygame.draw.rect(self.screen, HIGH, (origin[0] * self.square_size, origin[1] * self.square_size, self.square_size, self.square_size))

	def draw_message(self, message):
		"""
		Draws message to the screen. 
		"""
		self.message = True
		self.font_obj = pygame.font.Font('freesansbold.ttf', 44)
		self.text_surface_obj = self.font_obj.render(message, True, HIGH, BLACK)
		self.text_rect_obj = self.text_surface_obj.get_rect()
		self.text_rect_obj.center = (self.window_size / 2, self.window_size / 2)

class Board:
	def __init__(self):
		self.matrix = self.new_board()

	def new_board(self):
		"""
		Create a new board matrix.
		"""

		# initialize squares and place them in matrix

		matrix = [[None] * 8 for i in range(8)]

		# The following code block has been adapted from
		# http://itgirl.dreamhosters.com/itgirlgames/games/Program%20Leaders/ClareR/Checkers/checkers.py
		for x in range(8):
			for y in range(8):
				if (x % 2 != 0) and (y % 2 == 0):
					matrix[y][x] = Square(WHITE)
				elif (x % 2 != 0) and (y % 2 != 0):
					matrix[y][x] = Square(BLACK)
				elif (x % 2 == 0) and (y % 2 != 0):
					matrix[y][x] = Square(WHITE)
				elif (x % 2 == 0) and (y % 2 == 0): 
					matrix[y][x] = Square(BLACK)

		# initialize the pieces and put them in the appropriate squares

		for x in range(8):
			for y in range(3):
				if matrix[x][y].color == BLACK:
					matrix[x][y].occupant = Piece(RED)
			for y in range(5, 8):
				if matrix[x][y].color == BLACK:
					matrix[x][y].occupant = Piece(BLUE)

		return matrix

	def board_string(self, board):
		"""
		Takes a board and returns a matrix of the board space colors. Used for testing new_board()
		"""

		board_string = [[None] * 8] * 8 

		for x in range(8):
			for y in range(8):
				if board[x][y].color == WHITE:
					board_string[x][y] = "WHITE"
				else:
					board_string[x][y] = "BLACK"


		return board_string
	
	def rel(self, dir, loc):
		"""
		Returns the coordinates one square in a different direction to (x,y).

		===DOCTESTS===

		>>> board = Board()

		>>> board.rel(NORTHWEST, (1,2))
		(0,1)

		>>> board.rel(SOUTHEAST, (3,4))
		(4,5)

		>>> board.rel(NORTHEAST, (3,6))
		(4,5)

		>>> board.rel(SOUTHWEST, (2,5))
		(1,6)
		"""
		if dir == NORTHWEST:
			return (loc[0] - 1, loc[1] - 1)
		elif dir == NORTHEAST:
			return (loc[0] + 1, loc[1] - 1)
		elif dir == SOUTHWEST:
			return (loc[0] - 1, loc[1] + 1)
		elif dir == SOUTHEAST:
			return (loc[0] + 1, loc[1] + 1)
		else:
			return 0

	def adjacent(self, loc):
		"""
		Returns a list of squares locations that are adjacent (on a diagonal) to loc.
		"""

		return [self.rel(NORTHWEST, loc), self.rel(NORTHEAST, loc), self.rel(SOUTHWEST, loc), self.rel(SOUTHEAST, loc)]

	#edit
	def location(self, loc):
		"""
		Takes a set of coordinates as arguments and returns self.matrix[loc[0]][loc[1]]
		This can be faster than writing something like self.matrix[coords[0]][coords[1]]
		"""		
		return self.matrix[loc[0]][loc[1]]

	#edit
	def blind_legal_moves(self, loc):
		"""
		Returns a list of blind legal move locations from a set of coordinates loc on the board. 
		If that location is empty, then blind_legal_moves() return an empty list.
		"""

		if self.matrix[loc[0]][loc[1]].occupant != None:
			
			if self.matrix[loc[0]][loc[1]].occupant.king == False and self.matrix[loc[0]][loc[1]].occupant.color == BLUE:
				blind_legal_moves = [self.rel(NORTHWEST, loc), self.rel(NORTHEAST, loc)]
				
			elif self.matrix[loc[0]][loc[1]].occupant.king == False and self.matrix[loc[0]][loc[1]].occupant.color == RED:
				blind_legal_moves = [self.rel(SOUTHWEST, loc), self.rel(SOUTHEAST, loc)]

			else:
				blind_legal_moves = [self.rel(NORTHWEST, loc), self.rel(NORTHEAST, loc), self.rel(SOUTHWEST, loc), self.rel(SOUTHEAST, loc)]

		else:
			blind_legal_moves = []

		return blind_legal_moves

	#edit
	def legal_moves(self, loc, hop = False):
		"""
		Returns a list of legal move locations from a given set of coordinates loc on the board.
		If that location is empty, then legal_moves() returns an empty list.
		"""

		blind_legal_moves = self.blind_legal_moves(loc) 
		legal_moves = []
		legal_moves_hop = []

		if hop == False:
			for move in blind_legal_moves:
				if hop == False:
					if self.on_board(move):
						if self.location(move).occupant == None:
							legal_moves.append(move)

						elif self.location(move).occupant.color != self.location(loc).occupant.color and self.on_board(tuple(map(lambda i, j: i + (i - j), move, loc))) and self.location(tuple(map(lambda i, j: i + (i - j), move, loc))).occupant == None: # is this location filled by an enemy piece?
							
							legal_moves_hop.append(tuple(map(lambda i, j: i + (i - j), move, loc))) 

		else: # hop == True
			for move in blind_legal_moves:
				if self.on_board(move) and self.location(move).occupant != None:	#edit tuple(map(lambda i, j: i + (i - j), move, loc)) replaces (move[0] + (move[0] - x), move[1] + (move[1] - y))
					if self.location(move).occupant.color != self.location(loc).occupant.color and self.on_board(tuple(map(lambda i, j: i + (i - j), move, loc))) and self.location(tuple(map(lambda i, j: i + (i - j), move, loc))).occupant == None: # is this location filled by an enemy piece?
						legal_moves_hop.append(tuple(map(lambda i, j: i + (i - j), move, loc)))
		
		

		if legal_moves_hop:
			return legal_moves_hop
		else:
			return legal_moves

	#added by William Ament
	#scan through all peices, call legal_moves. If any are hop moves, those peices MUST be played
	#called in the end_turn(), for the side that will play next

	def legal_pieces(self, turn):
		legal_pieces = [] #every piece that can move
		legal_pieces_hop = [] #every piece that can hop

		for x in range(8):
			for y in range(8):
				if self.location((x,y)).occupant != None and self.location((x,y)).occupant.color == turn:
					blind_legal_moves = self.blind_legal_moves((x,y)) 
					legal_pieces.append((x,y))
					for move in blind_legal_moves:
						if self.on_board(move) and self.location(move).occupant != None:	#edit tuple(map(lambda i, j: i + (i - j), move, loc)) replaces (move[0] + (move[0] - x), move[1] + (move[1] - y))
							if self.location(move).occupant.color != self.location((x,y)).occupant.color and self.on_board(tuple(map(lambda i, j: i + (i - j), move, (x,y)))) and self.location(tuple(map(lambda i, j: i + (i - j), move, (x,y)))).occupant == None: # is this location filled by an enemy piece?
								legal_pieces_hop.append((x,y))
		
		if legal_pieces_hop:
			return legal_pieces_hop
		else:
			return legal_pieces
		
	

	#edit
	def remove_piece(self, loc):
		"""
		Removes a piece from the board at position loc. 
		"""
		self.matrix[loc[0]][loc[1]].occupant = None

	#edit 
	def move_piece(self, start, end):
		"""
		Move a piece from (start_x, start_y) to (end_x, end_y).
		"""

		self.matrix[end[0]][end[1]].occupant = self.matrix[start[0]][start[1]].occupant
		self.remove_piece((start[0], start[1]))

		self.king((end[0], end[1]))

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

	#edit
	def on_board(self, loc):
		"""
		Checks to see if the given square loc lies on the board.
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

		if loc[0] < 0 or loc[1] < 0 or loc[0] > 7 or loc[1] > 7:
			return False
		else:
			return True

	#edit
	def king(self, loc):
		"""
		Takes in (x,y), the coordinates of square to be considered for kinging.
		If it meets the criteria, then king() kings the piece in that square and kings it.
		"""
		if self.location(loc).occupant != None:
			if (self.location(loc).occupant.color == BLUE and loc[1] == 0) or (self.location(loc).occupant.color == RED and loc[1] == 7):
				self.location(loc).occupant.king = True 

class Piece:
	def __init__(self, color, king = False):
		self.color = color
		self.king = king

class Square:
	def __init__(self, color, occupant = None):
		self.color = color # color is either BLACK or WHITE
		self.occupant = occupant # occupant is a Piece object

def main():
	game = Game()
	game.main()

if __name__ == "__main__":
	main()