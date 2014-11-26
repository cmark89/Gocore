#!/usr/bin/python

import socket
import cPickle

columns = "ABCDEFGHIJKLMNOPQRS"
rows = range(1,20)

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
		message = self.recv(1024).decode('utf-8')
		parse_message(message)

	def parse_message(self, message):
		if message[0] == "B":
			# The server is sending an updated board state
			raw_board = self.socket.read(1024)
			self.board = pickle.loads(raw_board)
		elif message[0] == "T":
			# The server says that it is our turn
			prompt_turn()
		elif message[0] == "E":
			# The server says that the game is over
		elif message[0] == "X":
			# The message is sending an error

	def prompt_turn(self):
		self.error = ""
		while True:
			# Print the board state
			self.board.print_board()
			print("Choose a space.  Enter nothing to pass.")
			print(self.error)
			space = input("> ")
			if len(space.trim() == 0 or is_valid_space(space):
				break
	
	def is_valid_space(self, space):
		# Here we check the space input for validity and that space
		# against the board
		if not (space[0] in columns and space[1] in rows):
			self.error = "-----INVALID SPACE-----"
			return False
		else:
			# Check input against the board to ensure validity


