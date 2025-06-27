*********************************************
python3 mychatserver.py 
Server listening on 127.0.0.1:12000
New connection from ('127.0.0.1', 49935)
New connection from ('127.0.0.1', 49937)
New connection from ('127.0.0.1', 49939)
Client 49935 disconnected.
Client 49937 disconnected.
Client 49939 disconnected.
*********************************************
python3 mychatclient.py
Connected to chat server. Type 'exit' to leave.
49939: Hello Everyone
49937: How Are You guys doing
Good.
exit
Disconnected from server.
*********************************************
python3 mychatclient.py
Connected to chat server. Type 'exit' to leave.
49939: Hello Everyone
How Are You guys doing
49935: Good.
exit
Disconnected from server.
*********************************************
python3 mychatclient.py
Connected to chat server. Type 'exit' to leave.
Hello Everyone
49937: How Are You guys doing
49935: Good.
exit
Disconnected from server.
*********************************************

Above is a run with a server and three clients, each set up with a TCP connection, they then have a short conversation and exit the chat room.