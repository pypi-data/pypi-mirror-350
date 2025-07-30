from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import socket
import urllib.parse

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, webserverautofile=False, custom_html_path=None, **kwargs):
        self.webserverautofile = webserverautofile
        self.custom_html_path = custom_html_path
        self.directory = directory if directory else os.getcwd()
        super().__init__(*args, directory=self.directory, **kwargs)

    def do_GET(self):
        if self.webserverautofile:
            # Slúži na servovanie statických súborov z priečinka
            super().do_GET()
        else:
            # Ak je vypnutý autofile, zobrazí sa buď custom_html_path, alebo formulár
            if self.custom_html_path and os.path.isfile(self.custom_html_path):
                try:
                    with open(self.custom_html_path, 'rb') as f:
                        content = f.read()
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(content)
                except Exception as e:
                    self.send_error(500, f"Error loading file: {e}")
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                html = """
                <html><body>
                    <h1>Enter a command to save to file</h1>
                    <form method="POST" action="/">
                        <input type="text" name="command" required>
                        <input type="submit" value="Save">
                    </form>
                </body></html>
                """
                self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')

        try:
            params = urllib.parse.parse_qs(post_data)
            command = params.get('command', [''])[0]

            with open("output.txt", "w", encoding='utf-8') as f:
                f.write(command)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response = f"<html><body><h2>Saved:</h2><p>{command}</p><a href='/'>Back</a></body></html>"
            self.wfile.write(response.encode('utf-8'))

        except Exception as e:
            self.send_error(500, f"Error: {e}")

class EasyHTTPServer:
    def __init__(self, ip='auto', port=8080, webserverautofile=False, webdir=None, custom_html_path=None):
        self.port = port
        self.webserverautofile = webserverautofile
        self.webdir = webdir if webdir else os.getcwd()
        self.custom_html_path = custom_html_path
        self.ip = self.resolve_ip(ip)

    def resolve_ip(self, ip):
        if ip == 'localhost':
            return '127.0.0.1'
        elif ip == 'auto':
            return self.get_local_ip()
        else:
            # Predpokladá, že používateľ zadal platnú IP adresu
            return ip

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Spojenie na adresu mimo siete len na zistenie lokálnej IP
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def start(self):
        print(f"✅ Server is running at http://{self.ip}:{self.port} (autofile={self.webserverautofile})")

        def handler(*args, **kwargs):
            return CustomHTTPRequestHandler(
                *args,
                directory=self.webdir,
                webserverautofile=self.webserverautofile,
                custom_html_path=self.custom_html_path,
                **kwargs
            )

        httpd = HTTPServer((self.ip, self.port), handler)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n⛔️ Server stopped.")
            httpd.server_close()
