import socket
import json

class GameClient:
    def __init__(self, host, port):
        self.server_address = (host, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)

    def send_data(self, data):
        data_string = json.dumps(data)
        self.client_socket.sendall(data_string.encode())

    def receive_data(self):
        data = self.client_socket.recv(1024).decode()
        return json.loads(data)

    def close(self):
        self.client_socket.close()

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12345

    client = GameClient(HOST, PORT)

    # Example of sending data to the server
    data_to_send = {"player_position": (100, 200), "player_shooting": True}
    client.send_data(data_to_send)

    # Example of receiving data from the server
    received_data = client.receive_data()
    print(received_data)

    client.close()