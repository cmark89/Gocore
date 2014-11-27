#!/usr/bin/python

import socket
import pickle

rows = "ABCDEFGHIJKLMNOPQRS"
columns = range(1,20)
color = ""


class Client:
	def __init__(self):
		pass

	def connect(self, hostname, port):
		self.socket = socket.socket()
		try:
			self.socket.connect((hostname, port))
		except:
			pass
		else:
			# Enter the main client loop
			self.main_loop()

	def main_loop(self):
		# Try to read a value from the server and then act on it
		message = self.socket.recv(1024).decode('utf-8')
		self.parse_message(message)

	def parse_message(self, message):
		if message[0] == "S":
			# The server is sending setup info
			if message[1] == "B":
				color = "Black"
			elif message[1] == "W":
				color = "White"

		if message[0] == "B":
			# The server is sending an updated board state
			raw_board = self.socket.read(1024)
			self.board = pickle.loads(raw_board)
		elif message[0] == "T":
			# The server says that it is our turn
			prompt_turn()
		elif message[0] == "E":
			# The server says that the game is over
			pass
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
			if len(space.trim()) == 0 or is_valid_space(space):
				self.send_message_to_server(space)
				break

	def send_message_to_server(self, message):
		self.socket.send(str.encode(self.input_to_point(space)))
	
	def input_to_point(self, space):
		x = 0
		y = 0
		x = space[1]
		for index, row in enumerate(rows):
			if space[0] == rows[index]:
				y = index + 1
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
