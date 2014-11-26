#!/usr/bin/python

import socket

class GocoreServer:
	board = Board()
	clients = {}
	def __init__(self, hostname, port):
		self.hostname = hostname
		self.port = port

	def start(self):
		# Bind a socket to the given port and launch the 
		# connection thread
		s = socket.socket()
		s.bind(self.hostname, self.socket)
		s.listen(2)
		while(len(self.clients) < 2):
			c_socket, addr = s.accept()
			on_connection(c_socket, addr)
		self.main_loop()

	def on_connection(self, client_socket, addr):
		self.clients[client_socket] = addr

	def main_loop():
		
