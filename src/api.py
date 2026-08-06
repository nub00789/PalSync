import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

_status_provider = None


def register_status_provider(provider):
    global _status_provider
    _status_provider = provider


def get_status():

    if _status_provider is None:
        return {
            "name": "",
            "hosting": False,
            "running": False,
            "sync": 0,
        }

    return _status_provider()


class StatusHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path != "/status":
            self.send_response(404)
            self.end_headers()
            return

        body = json.dumps(get_status()).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)

    def log_message(self, *args):
        return


_server = None


def start_api(host="0.0.0.0", port=45678):

    global _server

    if _server is not None:
        return

    _server = ThreadingHTTPServer((host, port), StatusHandler)

    thread = threading.Thread(
        target=_server.serve_forever,
        daemon=True,
        name="PalSyncAPI",
    )

    thread.start()


def stop_api():

    global _server

    if _server is None:
        return

    _server.shutdown()
    _server.server_close()
    _server = None