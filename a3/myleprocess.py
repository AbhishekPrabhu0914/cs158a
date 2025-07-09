import socket
import threading
import uuid
import json
import time
from dataclasses import dataclass, asdict
import sys

@dataclass
class Message:
    uuid: str
    flag: int  # 0 = election ongoing, 1 = leader elected

class Node:
    def __init__(self, config_file="config.txt"):
        with open(config_file) as f:
            lines = f.read().splitlines()
            self.server_ip, self.server_port = lines[0].split(',')
            self.client_ip, self.client_port = lines[1].split(',')

        self.server_port = int(self.server_port)
        self.client_port = int(self.client_port)

        self.uuid = str(uuid.uuid4())
        self.state = 0  # 0 = election ongoing, 1 = leader known
        self.leader_id = None

        self.server_socket = None
        self.client_socket = None
        self.conn = None

        self.client_ready = threading.Event()

        self.log_file = f"log{self.server_port - 5000}.txt"
        self.log_lock = threading.Lock()

        # Clear previous log
        open(self.log_file, 'w').close()

    def log(self, message):
        with self.log_lock:
            with open(self.log_file, 'a') as f:
                f.write(message + '\n')

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen(1)
        self.conn, _ = self.server_socket.accept()
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def connect_to_server(self):
        connected = False
        while not connected:
            try:
                self.log(f"Attempting to connect to {self.client_ip}:{self.client_port}")
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.client_ip, self.client_port))
                connected = True
            except Exception as e:
                self.log(f"Connection failed: {e}. Retrying in 1s...")
                time.sleep(1)

        self.client_ready.set()  # mark client connection ready
        initial_msg = Message(self.uuid, 0)
        self.send_message(initial_msg)

    def send_message(self, msg: Message):
        if not self.client_ready.is_set():
            self.log("Client not ready. Waiting before sending...")
            self.client_ready.wait()

        try:
            msg_str = json.dumps(asdict(msg)) + '\n'
            self.client_socket.sendall(msg_str.encode())
            self.log(f"Sent: uuid={msg.uuid}, flag={msg.flag}")
        except Exception as e:
            self.log(f"Failed to send message: {e}")

    def receive_messages(self):
        buffer = ""
        while True:
            try:
                data = self.conn.recv(1024).decode()
                if not data:
                    break
                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line:
                        self.handle_message(json.loads(line))
            except:
                break

    def handle_message(self, msg_dict):
        msg = Message(**msg_dict)
        comparison = self.compare_uuid(msg.uuid)
        state_str = f"{self.state}"
        if self.state == 1:
            state_str += f", leader_id={self.leader_id}"

        self.log(f"Received: uuid={msg.uuid}, flag={msg.flag}, {comparison}, {state_str}")

        if msg.flag == 1:
            if msg.uuid == self.uuid:
                self.log("Received own leader announcement. Terminating propagation.")
                return
            if self.state == 0:
                self.state = 1
                self.leader_id = msg.uuid
                self.send_message(msg)
            elif self.leader_id != msg.uuid:
                self.log(f"Ignored: uuid={msg.uuid}, reason=Leader already known and different.")
        elif msg.uuid == self.uuid:
            self.state = 1
            self.leader_id = self.uuid
            self.log(f"Leader is decided to {self.leader_id}.")
            self.send_message(Message(self.leader_id, 1))
        elif self.state == 0:
            if msg.uuid > self.uuid:
                self.send_message(msg)
            elif msg.uuid < self.uuid:
                self.log(f"Ignored: uuid={msg.uuid}, reason=UUID is smaller.")
        else:
            self.log(f"Ignored: uuid={msg.uuid}, reason=Unhandled case.")

    def compare_uuid(self, other_uuid):
        if other_uuid > self.uuid:
            return "greater"
        elif other_uuid < self.uuid:
            return "less"
        else:
            return "same"

    def run(self):
        threading.Thread(target=self.start_server, daemon=True).start()
        time.sleep(5)  # allow server to be ready
        self.connect_to_server()
        time.sleep(30)  # allow election to complete
        if self.state == 1:
            final_log = f"Leader is {self.leader_id}"
            self.log(final_log)
            print(final_log)

if __name__ == "__main__":
    config_file = sys.argv[1] if len(sys.argv) > 1 else "config.txt"
    node = Node(config_file)
    node.run()
