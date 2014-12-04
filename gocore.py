#!/usr/bin/python
from server import Server
from client import Client
import socket
import time

"""
Gocore - v0.01
This file provides a client-facing interface for starting the program.
From the menu, players can start a server or join an existing one."""


in_game = False

version_string = "v0.01"
error = ""

def clear_screen():
	for i in range(0,100):
		print("")

def show_menu():
	print("""
=======================
Welcome to Gocore %s
=======================

Please enter a command:
	H) Host a game
	J) Join a game
	X) Exit

%s

""" % (version_string, error))
def host_game():
	global in_game
	in_game = True
	port = input("Please select a port to host on: ")
	# Start a server on that port and then connect

	# Because we're hosting, create a server instance
	server = Server(socket.gethostname(), port)
	server.start()
	time.sleep(.5)

	client = Client()
	client.connect(socket.gethostname(), port)

def join_game():
	global in_game
	in_game = True
	host = input("Please enter the IP address to connect to: ")
	port = input("Please select a port to connect to: ")

	# Now create a client and connect to the server
	client = Client()
	client.connect(host, port)

commands = { 'H' : host_game, 'J' : join_game, 'X' : exit }

def menu_loop():
	show_menu()
	choice = input("> ")
	if choice.upper() in commands:
		error = ""
		commands[choice.upper()]()
	else:
		error = "Invalid command."

while True:
	if not in_game:
		clear_screen()
		menu_loop()
	else:
		time.sleep(1)
