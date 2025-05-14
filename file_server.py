import socket
import os

HOST = '0.0.0.0'
PORT = 10002

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Server listening on {PORT}')
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        request = conn.recv(1024).decode()
        command, filename = request.strip().split()

        if command == "GET" and os.path.isfile(filename):
            filesize = os.path.getsize(filename)
            conn.sendall(f"OK {filesize}\n".encode())
            with open(filename, "rb") as f:
                conn.sendfile(f)
        else:
            conn.sendall(f"ERROR File not found\n".encode())

