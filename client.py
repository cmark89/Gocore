#!/usr/bin/python

import socket
import pickle
import threading
from point import Point
from board import Board

columns = "ABCDEFGHIJKLMNOPQRS"
rows = range(1,20)

class Client:
	color = ""
	headless = False
	board = Board()

	def __init__(self, is_headless=False):
		self.headless = is_headless
		

	def connect(self, hostname, port):
		self.socket = socket.socket()
		self.socket.connect((hostname, port))
		# Enter the main client loop
		t = threading.Thread(target=self.main_loop)
		t.start()

	def main_loop(self):
		# Try to read a value from the server and then act on it
		self.playing = True
		while self.playing:
			print("Await signal")
			message = self.socket.recv(1024).decode('utf-8')
			self.parse_message(message)

	def parse_message(self, message):
		print("Client received message: " + str(message))
		if message[0] == "S":
			# The server is sending setup info
			if message[1] == "B":
				self.color = "Black"
			elif message[1] == "W":
				self.color = "White"

		if message[0] == "U":
			# The server is sending an update from the other player
			updater = ""
			if(self.color == "Black"):
				updater = "White"
			else:
				updater = "Black"
			print("UPDATE MESSAGE: " + message)
			point = Point(int(message[1]), int(message[3:]))
			self.board.place_stone(point, updater)
		elif message[0] == "T":
			# The server says that it is our turn
			if not self.headless:
				self.prompt_turn()
			else:
				return
		elif message[0] == "E" and self.playing:
			self.playing = False
			# The server says that the game is over
			self.socket.close()
			self.board.score_game()
			winner = self.board.get_winning_player()
			if winner[0] == self.color:
				print("===WINNER!!!===")
			else:
				print("===LOSER!!!===")
			print("\tBlack: %s\tWhite: %s"%\
				(self.board.score["Black"], str(float(self.board.score\
				["White"]))))
		elif message[0] == "X":
			# The message is sending an error
			pass

	def prompt_turn(self):
		self.error = ""
		while True:
			# Print the board state
			self.board.print_board()
			print("Choose a space.  Enter nothing to pass.")
			print(self.error)
			space = input("> ")
			if is_valid_space(space):
				self.place_stone(space)
				break
			elif len(space) == 0:
				self.pass_turn()
				break

	def pass_turn(self):
		self.send_message_to_server("P")

	def send_message_to_server(self, message):
		# Prepend the first letter of our color to the message
		message = self.color[0] + message
		print("Client: Send message " + str(message))
		if(message[1] == "M"):
			full_message = message[0:2] + self.input_to_point(message[2:])
			print("Client: Send move message: " + full_message)
			self.socket.send(str.encode(full_message))
				
		else:
			self.socket.send(str.encode(message))

	def place_stone(self, point_raw):
		point = self.coord_to_point(point_raw)
		if self.board.place_stone(point, self.color):
			# Tell the server we placed the stone
			message = "M" + point_raw
			self.send_message_to_server(message)
		else: 
			print("Invalid point.")

	def coord_to_point(self, point_raw):	
		translated = self.input_to_point(point_raw).split('-')
		return Point(int(translated[0]), int(translated[1]))
	
	def input_to_point(self, space):
		x = 0
		y = 0
		y = space[1:]
		for index, row in enumerate(columns):
			if space[0] == columns[index]:
				x = index + 1
		return str(x) + "-" + str(y)


	def is_valid_space(self, space):
		# Here we check the space input for validity and that space
		# against the board
		if not (space[0] in columns and space[1] in rows):
			self.error = "-----INVALID SPACE-----"
			return False
		else:
			return True
			# Check input against the board to ensure validity
