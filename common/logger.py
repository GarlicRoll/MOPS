import logging
import json
import socket
from datetime import datetime
import time


class TcpJsonHandler(logging.Handler):
    def __init__(self, host, port, retry_delay=2):
        super().__init__()
        self.host = host
        self.port = port
        self.retry_delay = retry_delay
        self.sock = None

    def _connect(self):
        while self.sock is None:
            try:
                self.sock = socket.create_connection((self.host, self.port))
            except ConnectionRefusedError:
                time.sleep(self.retry_delay)

    def emit(self, record):
        if self.sock is None:
            self._connect()

        log = {
            "@timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        try:
            self.sock.sendall((json.dumps(log) + "\n").encode("utf-8"))
        except (BrokenPipeError, ConnectionResetError):
            self.sock = None  # сбросить соединение, чтобы переподключиться
            self.emit(record)


def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = TcpJsonHandler("logstash", 5000)
    logger.addHandler(handler)
    return logger
