import socket
import struct

class Client():
    def __init__(self, _server_host, _server_port) -> None:
        self.server_host = _server_host
        self.server_port = _server_port
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_host, self.server_port))

    def send(self, message):
        self.socket.sendall(struct.pack('>h', len(message)))
        self.socket.sendall(message)

    def get(self, length_service_messsage = 2):
        msglen = struct.unpack('>h', self.socket.recv(length_service_messsage))[0]
        return self.socket.recv(msglen)

    def disconnect(self):
        if self.socket != None:
            self.socket.close()
            self.socket = None