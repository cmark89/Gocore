#!/usr/bin/python

class Stone:
	def __init__(self, board, point, owner):
		self.position = point
		self.liberties = list(filter(lambda x: board.point_is_empty(x), \
				board.get_adjacent_points(point)))
		self.owner = owner
