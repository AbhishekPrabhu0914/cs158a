import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 12000
BUF_SIZE = 1024

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(BUF_SIZE)
            if not data:
                print("Disconnected from server.")
                break
            print(data.decode())
        except:
            break

def send_messages(sock):
    while True:
        message = input()
        sock.sendall(message.encode())
        if message.lower() == "exit":
            print("Disconnected from server.")
            sock.close()
            sys.exit()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except Exception as e:
        print(f"Could not connect to server: {e}")
        return

    print("Connected to chat server. Type 'exit' to leave.")
    
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()
    send_messages(sock)

if __name__ == "__main__":
    main()
