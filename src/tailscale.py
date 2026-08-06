import subprocess


class Tailscale:

    def __init__(self):
        pass

    def status(self):

        try:

            result = subprocess.run(
                ["tailscale", "status"],
                capture_output=True,
                text=True,
                timeout=5
            )

            return result.stdout

        except Exception:

            return ""

    def online(self, hostname):

        output = self.status()

        for line in output.splitlines():

            if hostname.lower() in line.lower():

                if "offline" not in line.lower():

                    return True

        return False