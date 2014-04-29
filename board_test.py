"""
board_test.py

A small program designed to test a method for generating a checkers board.

Everest Witman -  2014
"""

matrix = [[None] * 8] * 8

for x in xrange(8):
	for y in xrange(8):
		if (x % 2 != 0) and (y % 2 == 0):
			matrix[y][x] = "BLACK"
		elif (x % 2 != 0) and (y % 2 != 0):
			matrix[y][x] = "WHITE"
		elif (x % 2 == 0) and (y % 2 != 0):
			matrix[y][x] = "BLACK"
		elif (x % 2 == 0) and (y % 2 == 0): 
			matrix[y][x] = "WHITE"

print matrix