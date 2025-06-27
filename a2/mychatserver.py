import socket
import threading

HOST = '127.0.0.1'
PORT = 12000
BUF_SIZE = 1024

clients = {}  # Dictionary to store client sockets with their port numbers

def sendMessage(message, sender_port):
    for port, client_sock in clients.items():
        if port != sender_port:
            try:
                client_sock.sendall(f"{sender_port}: {message}".encode())
            except:
                pass  # In case of error, skip that client

def handle_client(client_sock, addr):
    port = addr[1]
    clients[port] = client_sock
    print(f"New connection from {addr}")
    
    try:
        while True:
            data = client_sock.recv(BUF_SIZE)
            if not data:
                break
            message = data.decode().strip()
            if message.lower() == "exit":
                break
            sendMessage(message, port)
    finally:
        print(f"Client {port} disconnected.")
        client_sock.close()
        del clients[port]

def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((HOST, PORT))
    server_sock.listen()
    print(f"Server listening on {HOST}:{PORT}")

    try:
        while True:
            client_sock, addr = server_sock.accept()
            threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\nServer shutting down.")
    finally:
        server_sock.close()

if __name__ == "__main__":
    main()
