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
	black.send_message_to_server("MA1")
	time.sleep(1)
	white.send_message_to_server("MA2")
	time.sleep(1)
	black.send_message_to_server("MG17")
	time.sleep(1)
	white.send_message_to_server("MB1")
	time.sleep(1)

	server.board.print_board()

	print("\nBLACK BOARD: ")
	black.board.print_board()

	print("\nWHITE BOARD: ")
	white.board.print_board()
