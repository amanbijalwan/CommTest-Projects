import socket

HOST = "192.168.1.50"  # ESP32 IP, check and update...
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        cmd = input(">>> ")
        s.sendall((cmd + "\n").encode())
        if cmd.lower() == "exit":
            break
        data = s.recv(1024).decode()
        print(data)
