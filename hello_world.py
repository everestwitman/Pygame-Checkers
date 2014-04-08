"""
hello_world.py

The equivelant of a "Hello, World!" program for the pygame libraries.

Everest Witman - 2014 - Marlboro College - Programming Workshop
"""

import pygame, sys 
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400,300)) # make a window with dimensions (400,300)
pygame.display.set_caption("Hello, World!") # set the caption text to be "Hello, World!"

while True: # main game loop
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.update()