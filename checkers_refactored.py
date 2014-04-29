import pygame, sys
from pygame.locals import *

class Game:
	def __init__(self):
		self.graphics = Graphics()

	def setup(self):
		self.graphics.setup_window()

	def event_loop(self):
		for event in pygame.event.get():

			if event.type == QUIT:
				self.terminate_game()

	def update(self):
		 self.graphics.update_display()

	def terminate_game(self):
		pygame.quit()
		sys.exit

	def main(self):
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

	def setup_window(self):
		pygame.init()
		pygame.display.set_caption(self.caption)

	def update_display(self):
		self.screen.blit(self.background, (0,0))

		pygame.display.update()
		self.clock.tick(self.fps)

def main():
	game = Game()
	game.main()

main()