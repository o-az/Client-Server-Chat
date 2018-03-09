# !/usr/bin/python
# author: Omar Bin Salamah
# Intro to Networks and their Applications HW2
# server.py

import itertools
import socket
import sys
import threading
import logging as log


class Server:

	my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket object
	connections = []  # keep track of connections
	buffer = 1028

	def __init__(self):

		self.count = itertools.count()  # indicate how many users are online

		self.my_socket.bind(('0.0.0.0', int(sys.argv[1])))  # binding. argv[1] is the port
		self.my_socket.listen(10)  # wait for connection from client

	''' Handle multiple users to be used in threading '''
	def handler(self, client, address):

		while True:
			global data
			data = client.recv(self.buffer)

			try:
				print('server received a message from {0} '.format(data.decode()[0:]))
			except IndexError:
				print("someone left the chat. Currently {0} online users".
				      format(len(self.connections)))

			for connection in self.connections:
				connection.send(data)

			if not data:  # msg indicating a user has exited
				print(str(address), 'has left this chat')

				self.connections.remove(client)  # remove client once there's no more data
				client.close()
				break

	def run(self):

		while True:

			connection, address = self.my_socket.accept()  # establish connection with client
			print("received data form: ", address)
			cThread = threading.Thread(target = self.handler, args = (connection, address))
			cThread.daemon = True
			cThread.start()

			self.connections.append(connection)  # append to connections for group chat


def main():

	print("------ server connection has been established ------")
	server = Server()
	server.run()


if __name__ == "__main__":
	if len(sys.argv) < 2 or sys.argv[1].isalpha():  # check terminal arguments

		print("\n _________________________________________\n"
		      "| You must use 1 argument after .py file  |\n"
		      "| FORMAT: server.py [PORT]                |\n"
		      "| example: server.py 10000                |\n"
		      "|_________________________________________|\n")
		sys.exit(0)
	try:
		main()

	except OSError as e: # if Address is already in use
		print(sys.argv[1], 'This port is being used right now. Use a different port...')

	except KeyboardInterrupt as e:  # CTRL + C to exit. Prompt a goodbye message :)
		print('\n\nThank you for using our server. Have a good day/night :)\n\n')
