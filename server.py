#!/usr/bin/python

import socket
from board import *
from point import *
import threading

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
		self.socket = s
		s.bind((self.hostname, int(self.port)))
		s.listen(2)
		while(len(self.clients) < 2):
			c_socket, addr = s.accept()
			self.on_connection(c_socket, addr)
		self.main_loop()

	def on_connection(self, client_socket, addr):
		self.clients.append(client_socket)

	def main_loop(self):
		# Begin the game!

		# Choose a player to be player one
		self.send(0, "SB")
		self.send(1, "SW")

		turn = 0
		while True:
			index = turn % 2
			# Tell this player whose turn it is
			self.clients[index].send(str.encode("T"))

			# Wait for input
			self.socket.recv(1024).decode('utf-8')

	
	def make_move(self, point, player):
		board.place_stone(point, player)
		board.history.append(board.board[:])

	def send(self, client, message):
		self.clients[client].send(str.encode(message))	
		
