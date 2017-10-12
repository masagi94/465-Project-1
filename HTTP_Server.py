#Hamza Tanveer
#Mauricio Salazar Giraldo
#Fall 2017-ECE 465 Project 1

import sys
import socket
#import socket module
from socket import *
from threading import *

#globals
threadArray = []


def main():

	mainThread = Thread(target = startServer, name = 'ServerThread')
	mainThread.setDaemon(True)
	threadArray.append(mainThread)
	threadArray[0].start()
	print("Server thread initiated.")

	serverQuit = False

	while not serverQuit:
		try:
			pass
		except KeyboardInterrupt:
			print("Exiting...")
			break


def startServer():

	if len(sys.argv) == 2: #take in 2 command line args
			portNumber = int(sys.argv[1]) #argv[1] b/c arg 0 and arg 1
	
	#prepare socket
	serverSocket = socket(AF_INET, SOCK_STREAM)

	# Listens in to the specified port number
	serverSocket.bind((gethostname(), portNumber))
	serverSocket.listen(1)

	clientIP = gethostbyname(gethostname())
	print("Client IP: " + clientIP)
	print("Press CTRL + c to exit.\n")


	while True:
		#establish connection
		connectionSocket, addr = serverSocket.accept()
		threadName = "Thread - " + str(len(threadArray))
		newThread = Thread(target = startConnectionThread, name = (threadName), args = [connectionSocket, addr])


		threadArray.append(newThread)
		newThread.start()

	serverSocket.close()

def startConnectionThread(connectionSocket, addr):
	try:
		message = connectionSocket.recv(4096)
		filename = message.split()[1]
		f = open(filename[1:])
		outputdata = f.read()

		#send 1 http header into socket
		connectionSocket.send("HTTP/1.1 200 OK\r\nContent-type:text/html;charset=utf8\r\n\r\n")

		#send content of req file to client
		for i in range (0,  len(outputdata)):
			connectionSocket.send(outputdata[i])
		connectionSocket.close()

	except IOError:
		#send resp for file not found
		connectionSocket.send("<!DOCTYPE html><html><body><h1>404 File Not Found</h1></body></html>")

		#close client socket
		connectionSocket.close()
	
main()