import socket
from _thread import *
import sys
import json

server = "192.168.8.112"
port = 2222

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))
    sys.exit()

s.listen(2)
print("Waiting for a connection, Server started")

pos = [(100, 300), (600, 300)]
bullets = [[], []]

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

def threaded_client(conn, player):
    try:
        conn.send(str.encode(make_pos(pos[player])))
    except Exception as e:
        print(f"Помилка при відправці початкової позиції: {e}")

    while True:
        try:
            data = conn.recv(2048).decode()
            if not data:
                print("Disconnected")
                break

            data = json.loads(data)
            pos[player] = data["player"]
            bullets[player] = data["bullets"]

            reply = {"player": pos[1 - player], "bullets": bullets[1 - player]}
            conn.sendall(json.dumps(reply).encode())
        except json.JSONDecodeError as e:
            print(f"Помилка при декодуванні JSON: {e}")
        except socket.error as e:
            print(f"Помилка сокету: {e}")
            break
        except Exception as e:
            print(f"Інша помилка: {e}")
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
