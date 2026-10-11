# server.py
import socket

HOST = "127.0.0.1" #"0.0.0.0"
PORT = 5001

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Server listening on {HOST}:{PORT}")
        conn, addr = s.accept()
        print(f"Connected by {addr}")
        conn.settimeout(1.0)  # avoid stuck behav.

        with conn:
            while True:
                try:
                    data = conn.recv(1024)
                except socket.timeout:
                    continue  # avoid blocking for now
                if not data:
                    break

                msg = data.decode().strip()
                if msg.lower() == "exit":
                    break
                elif msg.lower() == "status":
                    response = "Server status: running fine."
                else:
                    response = f"Server echo: {msg}"

                conn.sendall(response.encode())

if __name__ == "__main__":
    main()
