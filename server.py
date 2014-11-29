#!/usr/bin/python

import socket
from board import *
from point import *
import threading
import pickle

class GocoreServer:
	board = Board()
	clients = []
	pass_count = 0

	def __init__(self, hostname, port):
		self.hostname = hostname
		self.port = port

	def start(self):
		t = threading.Thread(target=self.__start)
		t.start()

	def __start(self):
		print("Starting server.")
		# Bind a socket to the given port and launch the 
		# connection thread
		s = socket.socket()
		s.bind((self.hostname, int(self.port)))
		s.listen(10)
		while(len(self.clients) < 2):
			print("Server: Awaiting connections")
			c_socket, addr = s.accept()
			self.on_connection(c_socket, addr)
			print("Server: Has %s clients" % (str(len(self.clients))))
		print("2 clients connected; initiate main loop")
		self.main_loop()

	def on_connection(self, client_socket, addr):
		self.clients.append(client_socket)

	def main_loop(self):
		# Begin the game!
		print("Server: initiate main loop")

		# Choose a player to be player one
		self.send(0, "SB")
		self.send(1, "SW")

		turn = 0
		while True:
			index = turn % 2

			# Tell this player whose turn it is
			print("Server send \"T\" to " + str(index))
			self.clients[index].send(str.encode("T"))

			# Wait for input
			sig = self.clients[index].recv(1024).decode('utf-8')
			print("SERVER GET SIGNAL: " + sig)
			self.process_signal(sig)

			turn += 1

	def process_signal(self, sig):
		owner = ""
		owner_index = 0
		if sig[0] == "B":
			owner = "Black"
		elif sig[0] == "W":
			owner = "White"
			owner_index = 1

		if sig[1] == "M":	# Making a move
			print("Server receiving move order")
			sig = sig[2:]
			self.make_move(Point(int(sig[0]), int(sig[2:])), owner)
			# Now tell the non-sending client to make the same move
			self.clients[(owner_index + 1) % 2].send\
				(str.encode("U"+sig[0] + "-" + sig[2:]))
	
	def make_move(self, point, player):
		print("Server play stone at point %s,%s for %s" %
			(point.x, point.y, player))
		self.board.place_stone(point, player)
		self.board.history.append(copy.deepcopy(self.board.board))

	def send(self, client, message):
		self.clients[client].send(str.encode(message))	
		
