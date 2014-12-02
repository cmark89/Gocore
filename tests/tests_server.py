#!/usr/bin/python
import server
import client
import socket
from server import GocoreServer
from client import Client
from random import randint
import time

def wait():
	time.sleep(.5)

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

	wait()

	black.place_stone("B1")
	wait()
	white.place_stone("E2")
	wait()
	black.place_stone("B2")
	wait()
	white.place_stone("E3")
	wait()

	black.place_stone("B3")
	wait()
	white.place_stone("E4")
	wait()
	black.place_stone("A4")
	wait()
	white.place_stone("F2")
	wait()

	black.place_stone("C3")
	wait()
	white.place_stone("F4")
	wait()
	black.place_stone("C4")
	wait()
	white.place_stone("G2")
	wait()

	black.place_stone("C5")
	wait()
	white.place_stone("G3")
	wait()
	black.place_stone("C6")
	wait()
	white.place_stone("G4")
	wait()

	black.pass_turn()
	white.pass_turn()
	server.board.print_board()

	print("\nBLACK BOARD: ")
	black.board.print_board()

	print("\nWHITE BOARD: ")
	white.board.print_board()
