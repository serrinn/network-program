import socket

HOST = '127.0.0.1'
PORT = 10002
FILENAME = 'example.txt'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(f"GET {FILENAME}\n".encode())
    response = s.recv(1024).decode()

    if response.startswith("OK"):
        _, length = response.split()
        length = int(length)
        received = b""
        while len(received) < length:
            data = s.recv(1024)
            if not data:
                break
            received += data
        with open("downloaded_" + FILENAME, "wb") as f:
            f.write(received)
    else:
        print("File not found")

