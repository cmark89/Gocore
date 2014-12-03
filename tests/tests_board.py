#!/usr/bin/python
import board
import point
def print_liberties(b):
	for sg in b.stone_groups:
		print("%s  L:%s" % (sg.owner, [str(x) for x in sg.liberties]))

def print_stone(s):
	print("%s - (%s,%s) - L:%s" % (s.owner, str(s.position.x), \
		str(s.position.y), [str(x) for x in s.liberties]))

def print_group(sg):
	for stone in sg.stones:
		print_stone(stone)

def print_groups(b):
	for g in b.stone_groups:
		print_group(g)

def test_board():
	b = board.Board()

	# PHASE 1 - Test placement
	print("Test 1: Placement")
	b.place_stone(point.Point(1,1), "White")
	b.place_stone(point.Point(1,2), "Black")
	b.print_board()
	
	assert(b.board[0][0] == "O")
	assert(b.board[0][1] == "X")

	print("Test 1 passed.")

	# PHASE 2 - Test simple capture
	print("Test 2: Capture")
	assert(len(b.stone_groups) == 2)
	b.place_stone(point.Point(2,1), "Black")
	b.print_board()
	assert(len(b.stone_groups) == 2)
	b.print_board()
	assert(b.board[0][0] == "-")
	print ("Test 2 passed.")

	# PHASE 3 - Test group cohesiveness
	print("Test 3: Group formation")
	b.place_stone(point.Point(2,2), "Black")
	b.print_board()
	print(len(b.stone_groups))
	assert(len(b.stone_groups) == 1)
	print("Test 3 passed.")

	# PHASE 4 - Test no-liberty move legality
	print("Test 4: Move legality 1")
	assert(not b.place_stone(point.Point(1,1), "White"))
	assert(b.place_stone(point.Point(1,1), "Black"))
	b.print_board()
	print("Test 4 passed.")

	# PHASE 5 - Test playing in the same location
	print("Test 5: Move legality 2")
	b.place_stone(point.Point(6,6), "White")
	assert(not b.place_stone(point.Point(6,6,), "White"))
	assert(not b.place_stone(point.Point(6,6,), "Black"))
	assert(len(b.stone_groups) == 2)
	b.print_board()
	print("Test 5 passed")

	# PHASE 6 - Kou
	print("Test 6: Kou")
	b.place_stone(point.Point(10,14), "White")
	b.place_stone(point.Point(9,15), "White")
	b.place_stone(point.Point(10,16), "White")
	b.place_stone(point.Point(11,15), "White")
	b.place_stone(point.Point(11,14), "Black")
	b.place_stone(point.Point(12,15), "Black")
	b.place_stone(point.Point(11,16), "Black")

	assert(b.place_stone(point.Point(10,15), "Black"))	# Takes white's stone
	b.print_board()
	assert(not b.place_stone(point.Point(11,15), "White")) #KOH!
	b.print_board()
	print("Test 6 passed")
