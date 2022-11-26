import socket
from threading import Thread
import struct
import json

import time

from lib_interpreter.interpreter import *

class Server:

    def __init__(self, _host, _port, _length_service_messsage = 2):
        self.socket = None
        self.host = _host
        self.port = _port
        self.length_service_messsage = _length_service_messsage
        self.clients = []

    def send(self, c_socket, message):
        c_socket.sendall(struct.pack('>h', len(message)))
        c_socket.sendall(message)

    def get(self, c_socket):
        msglen = struct.unpack('>h', c_socket.recv(self.length_service_messsage))[0]
        return c_socket.recv(msglen)

    def _process_client(self, c_socket, c_addr):
        try:
            with c_socket:
                interp = Interpreter()

                while True:
                    try:
                        data = self.get(c_socket)
                        # print(data)
                        data = json.loads(data)
                        mode, command = (*data,)
                        try:
                            if mode == 1:
                                result = interp.eval(command)
                            elif mode == 2:
                                result = interp.eval(command, return_tree = True)[1]
                            else:
                                result = interp.eval(command, return_variables = True)[1]

                            self.send(c_socket, json.dumps(result).encode())

                        except (InterpreterException, ParserException, LexerException) as e: 
                            self.send(c_socket, json.dumps(e.__str__()).encode())
                    except BlockingIOError:
                        time.sleep(0.2)
                        continue
                    except (ValueError, TypeError):
                        self.send(c_socket, json.dumps("None [JSON serialize error]").encode())
                        continue
                    # if not data:
                    #     break
        except Exception as e:
            print(f"\n!> Eexception ({type(e)}) in process_client: {e}")
        finally:
            print(f"\n> Client socket closed {c_addr}")

    def start(self):
        self.clients = []   # threads
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                self.socket = s
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((self.host, self.port))
                s.setblocking(False)
                s.listen(3)

                print("> Server started\n", end="")

                while True:
                    print("\r> Wait for new client", end="")
                    try:
                        client_socket, client_addr = s.accept()
                        print(f"\n> New client accepted {client_addr}")

                        t = Thread(target=self._process_client, args=(client_socket, client_addr))
                        t.start()

                        self.clients.append(t)

                        for th in self.clients[:]:
                            if not th.is_alive():
                                print(f"\n> Client-thread killed ({th})")
                                self.clients.remove(th)
                    except BlockingIOError:
                        time.sleep(0.2)
        except:
            self.socket = None
            print("\n> Server stopped!")

    def stop(self):
        if self.socket != None:
            self.socket.close()
            self.socket = None
        else:
            print("The server has already been stopped")