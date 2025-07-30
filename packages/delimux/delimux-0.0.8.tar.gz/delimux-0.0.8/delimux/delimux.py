import socket

class DeliMUX:
    """
    Client for controlling a MUX36S08 device via socket protocol.

    Server is expected to run on delimux-cmtqo:60606
    and respond to newline-terminated commands like SET, GET, ENABLE, etc.
    """

    def __init__(self, host='delimux-cmtqo', port=60606, verbose=False) -> None:
        self.host = host
        self.port = port
        self.verbose = verbose
        # Here we map the patch cable lines (key) to the channel number of the MUX36S08
        # On the MUX36S08, we number the channels, starting from zero!
        self.line_to_channel = {1 : 3, 2 : 2, 3 : 1, 4: 0, 5 : 6, 6 : 5, 7 : 4}
        self.channel_to_line = {v: k for k, v in self.line_to_channel.items()}
        

    def _send_command(self, command: str) -> str:
        with socket.create_connection((self.host, self.port), timeout=5) as client:
            if self.verbose:
                print(f"Sending: {command!r}")
            client.sendall((command + "\r\n").encode())
            response = client.recv(1024).decode().strip()
            if self.verbose:
                print(f"Received: {response!r}")
            return response

    def setChannel(self, n: int) -> None:
        """ Sets the channel 
        
        Channel refers to the channel of the MUX36S08
        """
        assert 0 <= n < 8, "Channel must be between 0 and 7"
        return self._send_command(f"SET {n}")
    
    def setLine(self, n: int) -> None:
        """ Sets the line 
        
        Line refers to the patch-cable line, line 8 is GND
        """
        assert 0 < n < 8, "Channel must be between 1 and 7"
        return self._send_command(f"SET {self.line_to_channel[n]}")

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
    
    def getLine(self) -> int:
        return self.channel_to_line[self.getChannel()]

    def enable(self) -> None:
        return self._send_command("ENABLE")

    def disable(self) -> None:
        return self._send_command("DISABLE")