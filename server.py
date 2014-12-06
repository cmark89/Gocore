#!/usr/bin/python

import socket
from board import *
from point import *
import time
import threading
import pickle

class Server:
	board = Board()
	clients = []
	pass_count = 0

	def __init__(self, hostname, port):
		self.hostname = socket.gethostbyname(socket.gethostname())
		print("Start server as " + self.hostname)
		self.port = int(port)

	def start(self):
		t = threading.Thread(target=self.__start)
		t.start()

	def __start(self):
		print("Starting server.")
		# Bind a socket to the given port and launch the 
		# connection thread
		s = socket.socket()
		s.bind((self.hostname, int(self.port)))
		s.listen(2)
		print("Server: Awaiting connections")
		while(len(self.clients) < 2):
			c_socket, addr = s.accept()
			self.on_connection(c_socket, addr)
		self.main_loop()

	def on_connection(self, client_socket, addr):
		self.clients.append(client_socket)

	def main_loop(self):
		# Begin the game!
		#print("Server: initiate main loop")

		# Choose a player to be player one
		self.send(0, "SB")
		self.send(1, "SW")
		time.sleep(.35)

		turn = 0
		self.playing = True
		while self.playing:
			index = turn % 2

			# Tell this player whose turn it is
			#print("Server send \"T\" to " + str(index))
			self.clients[index].send(str.encode("T"))

			# Wait for input
			sig = self.clients[index].recv(1024).decode('utf-8')
			#print("SERVER GET SIGNAL: " + sig)
			self.process_signal(sig)

			turn += 1
			time.sleep(1)

	def process_signal(self, sig):
		owner = ""
		owner_index = 0
		if sig[0] == "B":
			owner = "Black"
		elif sig[0] == "W":
			owner = "White"
			owner_index = 1

		if sig[1] == "M":	# Making a move
			#print("Server receiving move order")
			self.pass_count = 0
			sig = sig[2:].split('-')
			self.make_move(Point(int(sig[0]), int(sig[1])), owner)
			# Now tell the non-sending client to make the same move
			self.clients[(owner_index + 1) % 2].send\
				(str.encode("U"+sig[0] + "-" + sig[1]))
		if sig[1] == "P":
			#print("Player passes.")
			self.pass_count += 1
			if self.pass_count >= 2:
				self.end_game()

	def end_game(self):
		self.playing = False
		# Send the end message to the players
		self.send(0, "E")
		self.send(1, "E")
		# Shut down the connections
		for c in self.clients:
			c.close()
		
		# Score the board, just for fun
		self.board.score_game()


	def make_move(self, point, player):
		#print("Server play stone at point %s,%s for %s" %
#			(point.x, point.y, player))
		self.board.place_stone(point, player)
		self.board.history.append(copy.deepcopy(self.board.board))


	def send(self, client, message):
		self.clients[client].send(str.encode(message))	
