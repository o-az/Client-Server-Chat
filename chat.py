# !/usr/bin/python
# author: Omar Bin Salamah
# Intro to Networks and their Applications HW2
# chat.py

import socket
import sys
import select


class Client:

	my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket object
	buffer = 1028

	def message(self):

		while True:

			client_name = self.name + ': '
			client_input = input()
			self.my_socket.send( (client_name + client_input).encode() )

	def __init__(self):

		self.my_socket.connect(('0.0.0.0', int(sys.argv[2])))
		self.name = input("Enter your name then hit ENTER twice to join chat: ")

		print("\n\n\n--------------------------------------------\n"
		      "You have successfully entered the chat room\n"
		      "   To exit anytime press ( CTRL + C )\n"
		      "        You may begin chatting now\n"
		      "--------------------------------------------\n\n\n")

	def run(self):

		while True:
			# Two possible events:
			# sys.stdin: Client has typed something through keyboard.
			# my_socket: Server has send a new message by some other client you.
			streams = [sys.stdin, self.my_socket]

			# monitor both the streams simultaneously for inputs.
			readable, writable, err = select.select(streams, [], [])

			# if server has sent a msg, readable will fill up.
			for sock in readable:
				if sock == self.my_socket:

					# receive data in our variable. Check if it is empty.
					data = sock.recv(self.buffer)

					if not data:
						break
					else:

						# Write data to stdout and give client prompt back.
						sys.stdout.write(data.decode('utf-8'))
						sys.stdout.write('\n>')
						sys.stdout.flush()

				# its not the server. Our client has typed something in.
				else:

					# Read message. Send it to server. Give prompt back to client.
					msg = sys.stdin.readline()

					if msg:
						self.my_socket.send(str(self.name + ': ' + msg).encode())
						sys.stdout.write('')
						sys.stdout.flush()


def main():

	client = Client()
	client.run()


if __name__ == "__main__":

	if len(sys.argv) < 3:
		print("\n\n\nYou must use 3 arguments after .py\n"
		      "FORMAT: app.py [-topic] [IP:PORT] [chat TOPIC]\n"
		      "or,\n"
		      "FORMAT: app.py [-direct] [PORT] [IP:PORT]\n"
		      "Example: python /Users/Omar/Desktop/Pythonstuff/chat.py -direct 10000 localhost:10000\n")
		sys.exit(0)

	try:
		main()

	except ConnectionRefusedError as e:  # if user tries to run client before running server
		print('\n!!!Run the server first!!!\n')
		sys.exit(0)

	except KeyboardInterrupt as e:  # CTRL + C to exit. Prompt a message instead of error message
		print("\n\n\nYou have exited this chat room! :)")
		sys.exit(0)
