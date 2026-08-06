import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


class LockClient:

    def __init__(self, timeout=2):
        self.timeout = timeout

    def request(self, ip, action, owner, port=45678):

        url = f"http://{ip}:{port}/world-lock"

        body = json.dumps({
            "action": action,
            "owner": owner
        }).encode("utf-8")

        request = Request(
            url,
            data=body,
            headers={
                "Content-Type": "application/json"
            },
            method="POST"
        )

        try:

            with urlopen(request, timeout=self.timeout) as response:
                return json.loads(
                    response.read().decode("utf-8")
                )

        except (URLError, HTTPError):
            return None

        except Exception:
            return None

    def acquire(self, ip, owner):
        return self.request(ip, "acquire", owner)

    def release(self, ip, owner):
        return self.request(ip, "release", owner)

    def heartbeat(self, ip, owner):
        return self.request(ip, "heartbeat", owner)