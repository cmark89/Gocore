#!/usr/bin/python

"""
Gocore - v0.01
This file provides a client-facing interface for starting the program.
From the menu, players can start a server or join an existing one."""

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
	port = input("Please select a port to host on: ")
	# Start a server on that port and then connect


def join_game():
	host = input("Please enter the IP address to connect to: ")
	port = input("Please select a port to connect to: ")

	# Because we're hosting, create a server instance
	server = Server(host, port)
	server.start()

	# Now create a client and connect to the server

commands = { 'H' : host_game, 'J' : join_game, 'X' : exit }

def menu_loop():
	show_menu()
	choice = input("> ")
	if choice.upper() in commands:
		error = ""
		commands[choice.upper()]()
	else
		error = "Invalid command."

while True:
	clear_screen()
	menu_loop()
