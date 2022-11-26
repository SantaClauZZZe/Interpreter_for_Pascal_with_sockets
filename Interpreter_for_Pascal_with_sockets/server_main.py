from lib_socket.server import *
from threading import Thread

server = Server("127.0.0.1", 7878)

print("Чтобы остановить сервер, введите любой символ\n\n-------------------\n")

t = Thread(target=server.start)
t.start()

char = input("")
server.stop()

t.join()
print("\n-------------------\n\nПрограмма завершенна!")