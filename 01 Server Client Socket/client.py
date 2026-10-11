# client test 01
import socket

HOST = "127.0.0.1"
PORT = 5001

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.settimeout(1.0)  # avoid blocking 
        print("Connected to server. Type commands (or 'exit' to quit).")

        while True:
            cmd = input(">>> ")
            s.sendall(cmd.encode())
            if cmd.lower() == "exit":
                break

            try:
                data = s.recv(4096).decode()
                if data:
                    print(data)
            except socket.timeout:
                print("(No response yet)")

if __name__ == "__main__":
    main()
