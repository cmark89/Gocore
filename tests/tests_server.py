#!/usr/bin/python
import server
import client
import socket
from server import GocoreServer
from client import Client
from random import randint
import time

def test_server():
	port = randint(4000, 40000)
	server = GocoreServer(socket.gethostname(), port)
	server.start()
	print("Server started successfully.")
	time.sleep(1)

	# Start the clients headless so they don't freeze awaiting input
	black = Client(True)
	black.connect(socket.gethostname(), port)
	print("Black connected successfully")

	white = Client(True)
	white.connect(socket.gethostname(), port)
	print("White connected successfully")

	time.sleep(1)
	black.place_stone("A1")
	time.sleep(1)
	white.place_stone("A2")
	time.sleep(1)
	black.place_stone("G17")
	time.sleep(1)
	white.place_stone("B1")
	time.sleep(1)

	server.board.print_board()

	print("\nBLACK BOARD: ")
	black.board.print_board()

	print("\nWHITE BOARD: ")
	white.board.print_board()
