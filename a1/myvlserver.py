from socket import *

serverPort = 12000
bufsize = 64
n = 2

# Create and bind TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print("Server is ready to receive...")

connectionSocket, addr = serverSocket.accept()
print(f"Connected from {addr[0]}")

message = connectionSocket.recv(bufsize).decode()

# First Message With N bytes showing length
total_bytes = int(message[:n])

#Rest of the Bytes
message = message[n:max(64-n, total_bytes-n)]
print(message, ".")
received_data = ""
#IF the first message is all the bytes
if(len(message) >= total_bytes):
    message = message[:total_bytes]
    received_data = message
#Otherwise read until we are done
else:
    received_data += message
    while len(received_data) < total_bytes:
        chunk = connectionSocket.recv(bufsize).decode()
        received_data += chunk

        print(f"processed: {received_data}")

#Ensure that we send exactly bufsize length messages
while len(received_data) % bufsize != 0:
    received_data += ' '
    
# Convert to uppercase
response = received_data.upper()
connectionSocket.send(response.encode())

print(f"Length of Message Sent: {len(response)}")
connectionSocket.close()
print("Connection closed\n")
