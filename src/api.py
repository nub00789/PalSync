import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from status_store import get


class StatusHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/status":

            body = json.dumps(get()).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()

            self.wfile.write(body)

            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, *args):
        pass


_server = None


def start_api(host="0.0.0.0", port=45678):

    global _server

    if _server is not None:
        return

    _server = ThreadingHTTPServer(
        (host, port),
        StatusHandler
    )

    threading.Thread(
        target=_server.serve_forever,
        daemon=True,
        name="PalSyncAPI",
    ).start()


def stop_api():

    global _server

    if _server is None:
        return

    _server.shutdown()
    _server.server_close()
    _server = None