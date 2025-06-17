from socket import *


#Constants for modularity
serverName = 'localhost'
serverPort = 12000
bufsize = 64
n = 2


clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# User input
text = input("Input lowercase sentence: ")
while len(text) % bufsize != 0:
    text += ' '

#Send only in bufsize chunks
clientSocket.send(text[0:bufsize].encode())

#Second chunk if necessary
if(len(text) > bufsize):
    clientSocket.send(text[bufsize:bufsize*2].encode())

# Receive response
response = ""
while True:
    chunk = clientSocket.recv(bufsize).decode()
    if not chunk:
        break
    response += chunk

print("From Server:", response)
clientSocket.close()
