import json
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


class APIClient:

    def __init__(self, timeout=1):
        self.timeout = timeout

    def status(self, ip, port=45678):

        try:

            with urlopen(
                f"http://{ip}:{port}/status",
                timeout=self.timeout
            ) as response:

                return json.loads(
                    response.read().decode("utf-8")
                )

        except (URLError, HTTPError):
            return None

        except Exception:
            return None