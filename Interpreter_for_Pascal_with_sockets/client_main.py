from lib_socket.client import *
import json

server_host = "127.0.0.1"
server_port = 7878

client = Client(server_host, server_port)
client.connect()

command = ''
mode = 1

while (True):
    command = input("> ")

    if command == "-h" or command == "--help":
        print("""Комманды: 
                 -h OR --help -> справка команд.
                 -e OR --exit -> выход из программы

                 Для выполнения кода на удаленном интерпретаторе просто введите его сюда и нажмите Enter

                 По умолчанию интерпретатор возвращает значение, возвращаемое выражением.
                 Дополнительные опции:
                    -rd OR --return_default -> Сделать возвращаемое значение по умолчанию
                    -rt OR --return_tree -> Сделать возвращаемое значение в виде исходного дерева на основе которого считается выходной результат.
                    -rv OR --return_var -> Сделать возвращаемое значение в виде словаря со значениями переменных,
                 """)
    elif command == "-e" or command == "--exit":
        break
    elif command == "-rd" or command == "--return_default":
        mode = 1
    elif command == "-rt" or command == "--return_tree":
        mode = 2
    elif command == "-rv" or command == "--return_var":
        mode = 3
    else:
        try:
            data = json.dumps([mode, command])
            data = data.encode()
            client.send(data)

            response = client.get()
            response = json.loads(response)
            print(f">> {response}")
        except:
            print("!> Сервер зыкрыл соединение")

print("Программа завершена")