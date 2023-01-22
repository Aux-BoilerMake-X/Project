import socket
import random


HOST = "172.20.10.4"
PORT = 5004


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        data = s.recv(1024)
        print(data)
        if random.randint(0, 5) == 3:
            s.sendall(b"Hello from client")
            print("sending data to server")