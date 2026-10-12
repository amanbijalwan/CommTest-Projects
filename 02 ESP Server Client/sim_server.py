import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

HOST = "127.0.0.1"
TCP_PORT = 5000
WEB_PORT = 8080

# --- TCP Socket Server ---
def tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, TCP_PORT))
        s.listen(1)
        print(f"[TCP] Listening on {HOST}:{TCP_PORT}")
        while True:
            conn, addr = s.accept()
            print(f"[TCP] Connected by {addr}")
            threading.Thread(target=handle_client, args=(conn,)).start()

def handle_client(conn):
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            cmd = data.decode().strip()
            if cmd.lower() == "exit":
                break
            elif cmd.lower() == "status":
                response = "Server status: running fine.\n"
            else:
                response = f"Server echo: {cmd}\n"
            conn.sendall(response.encode())

# --- Web Server ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        cmd = params.get("cmd", [""])[0]

        if cmd.lower() == "status":
            response = "Server status: running fine."
        elif cmd:
            response = f"Server echo: {cmd}"
        else:
            response = ("<form action='/' method='GET'>"
                        "Command: <input name='cmd'>"
                        "<input type='submit'>"
                        "</form>")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(response.encode())
            return

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response.encode())

def web_server():
    httpd = HTTPServer((HOST, WEB_PORT), SimpleHandler)
    print(f"[WEB] Serving on http://{HOST}:{WEB_PORT}")
    httpd.serve_forever()

# --- Run both servers ---
if __name__ == "__main__":
    threading.Thread(target=tcp_server, daemon=True).start()
    web_server()
