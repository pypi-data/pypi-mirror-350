import socket

class DeliMUX:
    """
    Client for controlling a MUX36S08 device via socket protocol.

    Server is expected to run on delimux-cmtqo:60606
    and respond to newline-terminated commands like SET, GET, ENABLE, etc.
    """

    def __init__(self, host='delimux-cmtqo', port=60606, verbose=False):
        self.host = host
        self.port = port
        self.verbose = verbose

    def _send_command(self, command: str) -> str:
        with socket.create_connection((self.host, self.port), timeout=5) as client:
            if self.verbose:
                print(f"Sending: {command!r}")
            client.sendall((command + "\r\n").encode())
            response = client.recv(1024).decode().strip()
            if self.verbose:
                print(f"Received: {response!r}")
            return response

    def setChannel(self, n: int):
        assert 0 <= n < 8, "Channel must be between 0 and 7"
        return self._send_command(f"SET {n}")

    def getState(self) -> list:
        resp = self._send_command("GET")
        if resp.startswith("STATE"):
            bits = resp.split()[1:]
            return [int(b) for b in bits]
        raise ValueError(f"Unexpected response: {resp}")

    def getChannel(self) -> int:
        resp = self._send_command("CHANNEL")
        if resp.startswith("CHANNEL"):
            return int(resp.split()[1])
        raise ValueError(f"Unexpected response: {resp}")

    def enable(self):
        return self._send_command("ENABLE")

    def disable(self):
        return self._send_command("DISABLE")