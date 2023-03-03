from __future__ import unicode_literals
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
from urllib.parse import parse_qs
import subprocess

hostName = "localhost"
serverPort = 8080

class MyServer(SimpleHTTPRequestHandler):
    def handle_download(self, url):
        if len(url) == 0:
            return
        
        source = subprocess.check_output(["yt-dlp", "--get-url", "-f", "bestaudio/best", url])
        source = source.decode()

        self.send_response(301)
        self.send_header("Location", source)
        self.end_headers()
        

    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        if "url" in query_components:
            self.handle_download(query_components["url"][0])
        else:
            pass

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")