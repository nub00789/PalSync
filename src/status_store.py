import threading

_lock = threading.Lock()

_status = {
    "name": "",
    "hosting": False,
    "running": False,
    "sync": 0,
}


def update(**kwargs):
    with _lock:
        _status.update(kwargs)


def get():
    with _lock:
        return dict(_status)