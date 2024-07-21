import socket
import json
from config import *

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(BUFFER_SIZE).decode()
        except Exception as e:
            print(f"Помилка при підключенні: {e}")
            return None

    def send(self, data):
        try:
            self.client.send(data.encode())
            return self.client.recv(BUFFER_SIZE).decode()
        except socket.error as e:
            print(f"Помилка при відправці/отриманні даних: {e}")
            return None
