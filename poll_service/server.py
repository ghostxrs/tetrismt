from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen
from threading import Timer
from os import getenv


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', int(getenv("PORT", default="8000")))
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


class Poll(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")


def ping():
    urlopen("https://tetris.cfapps.us10-001.hana.ondemand.com/").read()
    print("OK")
    Timer(3600.2, ping).start()


if __name__ == "__main__":
    ping()
    run(handler_class=Poll)
