#Hamza Tanveer
#Mauricio Salazar Giraldo
#Fall 2017-ECE 465 Project 1

"""
To run the code, type: 
	python HTTP_Server.py (desired port number)

The client ip address will be printed out on the console. Open up a 
web browser and type: 
	http://(client ip address):(port number)/HelloWorld.html

On the console, the thread number will print out, indicating the number of threads
dealt with.

Since it's multi-threaded, you may open different web browsers and re-type the URL
and you should get the same output.

If the inproper file name is typed, a "404 NOT FOUND" message will appear. If the
correct file name is typed, "Hello World!" will print out.

"""


import sys

from socket import *
from threading import *

#globals
threadArray = []
portNumber = 0 #simply to instantiate the value, it will be overwritten later



# Sets up the main thread, adds it to the array of threads

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

	# Prepares socket
	serverSocket = socket(AF_INET, SOCK_STREAM)

	# Listens in to the specified port number
	serverSocket.bind((gethostname(), portNumber))
	serverSocket.listen(1)

	clientIP = gethostbyname(gethostname())
	print("Client IP: " + clientIP)
	print("Ready to serve...\n")
	print("Press CTRL + c to exit.\n")


	'''
		Creates new threads as new requests come in. The accept() function returns a new address and a new port number for the
		connection that the kernel chooses. The two print statements print out the new port number, and the amount of threads created,
		confirming proper multithreading.
	'''
	while True:
		#Establishes a connection. accept() sets up the connection on a new port chosen by the kernel.
		connectionSocket, addr = serverSocket.accept()
		print >>sys.stderr, 'Ip address, New port number :\n', addr

		threadName = "Thread - " + str(len(threadArray))
		newThread = Thread(target = startConnectionThread, name = (threadName), args = [connectionSocket, addr])


		threadArray.append(newThread)
		print("Number of threads: %d\n\n") %len(threadArray)
		newThread.start()

	serverSocket.close()


def startConnectionThread(connectionSocket, addr):
	try:
		message = connectionSocket.recv(4096)
		filename = message.split()[1]
		f = open(filename[1:])
		outputdata = f.read()

		#send 1 http header into socket
		connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n")
		connectionSocket.send("<html><head></head><body><h1>Hello World!</h1></body></html>\r\n")

		#send content of req file to client
		#for i in range (0,  len(outputdata)):
		#	connectionSocket.send(outputdata[i])
		#connectionSocket.close()

	except IOError:
		#send resp for file not found
		connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n")
		connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")
		
		#close client socket
		connectionSocket.close()
	


if len(sys.argv) == 2: #take in 2 command line args
	portNumber = int(sys.argv[1]) #argv[1] b/c arg 0 and arg 1
	print("\nServer port: %d") % portNumber
else:
	print '\n Error:     Missing port number.\n Usage:     HTTP_Server.py <port number>'
	sys.exit(0)





main()