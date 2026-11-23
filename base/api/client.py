import random
import socket


class qrng:
    def __init__(self, host, port, timeout=3):
        self.client = socket.create_connection((host, port), timeout=timeout)

    def _receive_hex(self, command):
        try:
            self.client.sendall(str(command).encode("ascii"))
            payload = self.client.recv(4096)
            if not payload:
                raise ConnectionError("QRNG device returned no data")
            return payload.strip()
        finally:
            self.client.close()

    def getQrngDecimal(self, command):
        return int(self._receive_hex(command), 16)

    def getQrngArray(self, length):
        decimal = str(int(self._receive_hex(3), 16))
        output = []
        while len(output) < length:
            output.append(int(decimal[random.randrange(len(decimal))]))
        return output

    def getQrngHexArray(self, length, size):
        text = self._receive_hex(3).decode("ascii").strip()
        return [text[index : index + size] for index in range(0, len(text), size)][
            :length
        ]

    def getHexString(self):
        return self._receive_hex(1).decode("ascii")
