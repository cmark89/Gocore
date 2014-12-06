#!/usr/bin/python

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y
	def __hash__(self):
		return hash((self.x, self.y))
	def __str__(self):
		return str(self.x) + "," + str(self.y)
	def __repr__(self):
		return self.__str__()
