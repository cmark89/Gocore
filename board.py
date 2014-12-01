#!/usr/bin/python
from stone import *
from point import *
from stoneGroup import *
import copy

class Board:
	score = {"Black" : 0, "White" : 0}
	history = []
	def __init__(self):
		self.stone_groups = []
		self.create_board()
	

	def __eq__(self, other):
		# Check if the board situation (sans-score) is the same
		for row in self.board:
			for column in row:
				if column != other.board[row][column]:
					return False
		return True
	

	def create_board(self):
		# List comprehension to create a 2D board
		self.board = [['-' for x in range(0,19)] \
				for y in range(0,19)]


	def print_board(self):
		for y in range(0,19):
			for x in range(0, 19):
				last = " "
				if x == 18: last = "\n"
				print(self.board[x][y], end=last)


	def point_is_empty(self, point):
		return self.board[int(point.x)-1][int(point.y)-1] == '-'
	

	def get_adjacent_points(self, point):
		points = []
		points.append(Point(point.x-1, point.y))
		points.append(Point(point.x+1, point.y))
		points.append(Point(point.x, point.y-1))
		points.append(Point(point.x, point.y+1))
		points = list(filter(lambda p: p.x > 0 and p.x < 20 and p.y > 0 \
				and p.y < 20, points))
		return points

	def is_matching_board(self, other):
		for x, y in zip(range(0,19), range(0, 19)):
			print("COMPARE " + self.board[x][y] + \
				" : " + other[x][y])
			if self.board[x][y] != other[x][y]:
				print("Difference found; unidentical board")
				return False
		print("Identical board")
		return True
				
	def kou(self):
		for s in self.history:
			if self.is_matching_board(s):
				print("Kou state found")
				return True
		print("No kou")
		return False


	def update_board(self):
		self.board = [['-' for x in range(0,19)] for y in range(0,19)]
		for group in self.stone_groups:
			for s in group.stones:
				char = ""
				if s.owner == "White": char = "O"
				elif s.owner == "Black": char = "X"
				self.board[s.position.x - 1][s.position.y-1] = char

	# Returns True if the move is completed legally, False otherwise
	def place_stone(self, point, owner, simulation=False):
		if not self.point_is_empty(point):
			print("SOMETHING ALREADY HERE")
			return False;

		# We're in the real world, so we copy the boardstate and 
		# run a simulation of the move on it
		if not simulation:
			sim = copy.deepcopy(self)
			if not sim.place_stone(point,owner,True):
				# Encounter an error, so return right away
				print("Simulation encountered an error.")
				return False
			else:
				# The move returned successfully, so perform it for real
				del sim
		
		linked_groups = [] 
		# Update each group, removing this point from liberties for group in self.stone_groups:
		for group in self.stone_groups:
			for l in list(filter(lambda p: p.x == point.x and p.y == point.y, \
				group.liberties)):
				group.liberties.remove(l)
				if group.owner == owner:
					linked_groups.append(group)

		# Check each enemy group to see if they have zero liberties
		for group in list(filter(lambda x: x.owner != owner and \
				len(x.liberties) == 0, self.stone_groups)):
			# If so, remove and give points to this owner
			self.stone_groups.remove(group)
			self.score[owner] += len(group.stones)

		self.update_board()

		# Create a new stone group containing the point
		s = Stone(self, point, owner)
		stones = [s]

		# Loop through each group owned by this player and see if 
		# the new stone is in that group's liberties
		for group in linked_groups:
				stones += group.stones
				self.stone_groups.remove(group)

		# Finally, add the new group to the board
		newGroup = StoneGroup(self, stones)
		self.stone_groups.append(newGroup)

		# Check to see if the new group has any liberties
		# (Check after removing captures because it may create liberties)
		if len(newGroup.liberties) == 0:
			print("No liberties!  Cannot add.")
			return False #, "Illegal move (no liberties)"

		self.update_board()

		# TODO: Kou check
		return True
