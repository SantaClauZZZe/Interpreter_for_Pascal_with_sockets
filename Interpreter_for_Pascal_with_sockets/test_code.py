from lib_socket.server import *
from lib_socket.client import *

from threading import Thread
import time

import pytest

server_host = "127.0.0.1"
server_port = 7878

class Test_Interpreter_with_sockets:
    def test_code(self):
        server = Server(server_host, server_port)
        server.stop()
        t = Thread(target=server.start)
        t.start()
        time.sleep(0.25)

        killed_client = Client(server_host, server_port)
        killed_client.connect()
        time.sleep(0.250)
        killed_client.disconnect()
        time.sleep(0.150)

        client = Client(server_host, server_port)
        client.connect()
        time.sleep(0.250)

        client.send("RAW_STR_DATA".encode())

        response = client.get()
        response = json.loads(response)
        print(f">> {response}")

        data = json.dumps([1, "g;"])
        data = data.encode()
        client.send(data)

        response = client.get()
        response = json.loads(response)
        print(f">> {response}")

        data = json.dumps([1, "END;"])
        data = data.encode()
        client.send(data)

        response = client.get()
        response = json.loads(response)
        print(f">> {response}")

        data = json.dumps([1, "BEGIN"])
        data = data.encode()
        client.send(data)

        response = client.get()
        response = json.loads(response)
        print(f">> {response}")

        data = json.dumps([1, "BEGIN"])
        data = data.encode()
        client.send(data)

        response = client.get()
        response = json.loads(response)
        print(f">> {response}")

        data = json.dumps([2, "z:= 123 + 123 * 12 - 1 /        1;"])
        data = data.encode()
        client.send(data)

        response = client.get()
        response = json.loads(response)
        print(f">> {response}")

        data = json.dumps([2, "+(-z);"])
        data = data.encode()
        client.send(data)

        response = client.get()
        response = json.loads(response)
        print(f">> {response}")

        data = json.dumps([1, "+(-z);"])
        data = data.encode()
        client.send(data)

        response = client.get()
        response = json.loads(response)
        print(f">> {response}")

        data = json.dumps([3, "y"])
        data = data.encode()
        client.send(data)

        response = client.get()
        response = json.loads(response)
        print(f">> {response}")

        data = json.dumps([3, "y;"])
        data = data.encode()
        client.send(data)

        response = client.get()
        response = json.loads(response)
        print(f">> {response}")

        data = json.dumps([3, ""])
        data = data.encode()
        client.send(data)

        response = client.get()
        response = json.loads(response)
        print(f">> {response}")

        data = json.dumps([3, "z := :=;"])
        data = data.encode()
        client.send(data)

        response = client.get()
        response = json.loads(response)
        print(f">> {response}")

        data = json.dumps([3, "z = 2;"])
        data = data.encode()
        client.send(data)

        response = client.get()
        response = json.loads(response)
        print(f">> {response}")

        data = json.dumps([3, "z := *;"])
        data = data.encode()
        client.send(data)

        response = client.get()
        response = json.loads(response)
        print(f">> {response}")

        data = json.dumps([3, "z * 2;"])
        data = data.encode()
        client.send(data)

        response = client.get()
        response = json.loads(response)
        print(f">> {response}")

        data = json.dumps([2, "z :/= 2"])
        data = data.encode()
        client.send(data)

        response = client.get()
        response = json.loads(response)
        print(f">> {response}")

        data = json.dumps([1, "BEGIN"])
        data = data.encode()
        client.send(data)

        response = client.get()
        response = json.loads(response)
        print(f">> {response}")

        data = json.dumps([3, "END."])
        data = data.encode()
        client.send(data)

        response = client.get()
        response = json.loads(response)
        print(f">> {response}")

        data = json.dumps([1, "END."])
        data = data.encode()
        client.send(data)

        response = client.get()
        response = json.loads(response)
        print(f">> {response}")

        server.stop()
        t.join()

        parser = Parser()
        with pytest.raises(ParserException):
            parser.expr()
            
        with pytest.raises(ParserException):
            parser.assignment()
            
        with pytest.raises(ParserException):
            parser.statement()

        with pytest.raises(NotImplementedError):
            nd = NodeVisitor()
            nd.visit(None)

        return

obj = Test_Interpreter_with_sockets()
obj.test_code()