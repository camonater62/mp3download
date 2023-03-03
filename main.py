from __future__ import unicode_literals
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, unquote
import subprocess
from pathlib import PurePosixPath

hostName = "localhost"
serverPort = 8080

class MyServer(SimpleHTTPRequestHandler):
    def handle_download(self, url):
        try:
            url = unquote(url)

            source = subprocess.check_output(["yt-dlp", "--no-playlist", "--get-url", "-f", "bestaudio/best", url])
            source = source.decode()

            self.send_response(301)
            self.send_header("Location", source)
            self.end_headers()
        except:
            self.send_error(400)

    def do_GET(self):
        parts = PurePosixPath(
            unquote(
                urlparse(
                    self.path
                ).path
            )
        ).parts

        if (parts[1] == "ytdl"):
            self.handle_download(self.path[6:])

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")