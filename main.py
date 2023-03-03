from __future__ import unicode_literals
import yt_dlp as youtube_dl
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import time
from urllib.parse import urlparse
from urllib.parse import parse_qs
import os
import shutil

hostName = "192.168.1.138"
serverPort = 8080


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d["status"] == "finished":
        # print('Done downloading, now converting ...')
        pass


ydl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
    "outtmpl": "%(title)s.%(ext)s",
    "logger": MyLogger(),
    "noplaylist": True,
    "progress_hooks": [my_hook],
}


class MyServer(SimpleHTTPRequestHandler):
    def handle_download(self, url):
        if len(url) == 0:
            return

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(url)
            if meta["id"]:
                # Video exists
                filename = "{}.mp3".format(meta["title"])

                print("Downloading & Converting")
                while not os.path.isfile(filename):
                    time.sleep(0.1)

                print("Uploading")
                f = open(filename, "rb")

                filepath = (
                    os.path.basename(filename).encode("latin-1", "ignore").decode()
                )

                self.send_response(200)
                self.send_header("Content-type", "audio/mp3")
                self.send_header(
                    "Content-Disposition",
                    'attachment; filename="{}"'.format(filepath),
                )
                fs = os.fstat(f.fileno())
                self.send_header("Conent-Length", str(fs.st_size))
                self.end_headers()
                shutil.copyfileobj(f, self.wfile)

                f.close()
                os.remove(filename)
            else:
                self.send_error(404)

    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        if "url" in query_components:
            self.handle_download(query_components["url"][0])
        else:
            if self.path == "/":
                self.path = "index.html"
            return SimpleHTTPRequestHandler.do_GET(self)


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
