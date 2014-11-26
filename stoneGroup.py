#!/usr/bin/python

class StoneGroup:
	def __init__(self, board, stones):
		self.stones = stones
		self.liberties = []
		for s in stones:
			self.liberties += list(filter(lambda x: board.point_is_empty(x),\
				board.get_adjacent_points(s.position)))
		self.liberties = set(self.liberties)
		self.owner = self.stones[0].owner
