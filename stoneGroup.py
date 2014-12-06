#!/usr/bin/python

class StoneGroup:
	def __init__(self, board, stones):
		self.stones = stones
		self.liberties = []
		for s in stones:
			self.liberties += list(filter(lambda x: board.point_is_empty(x),\
				board.get_adjacent_points(s.position)))
		for s in self.stones:	
			for p in self.liberties[:]:
				if p.x == s.position.x and p.y == s.position.y:
					self.liberties.remove(p)
		
		self.liberties = set(self.liberties)
		self.owner = self.stones[0].owner
