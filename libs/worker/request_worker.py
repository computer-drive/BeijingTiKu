from PySide6.QtCore import QThread, Signal
from libs.consts import *
from .request import get_data

class RequestsWorker(QThread):
    finished = Signal(tuple)

    def __init__(self, url, args=None, headers=HEADERS, timeout=DEFAULT_TIMEOUT):
        super().__init__()

        self.url = url
        self.args = args
        self.headers = headers
        self.timeout = timeout

    def __run__(self):
        status, data = get_data(self.url, self.args, self.headers, self.timeout)

        return status, data