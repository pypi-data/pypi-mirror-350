from datetime import datetime
from abc import ABC, abstractmethod


class Stream(ABC):
    def __init__(self):
        pass


class OStream(Stream, ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def log(self, msg: str):
        pass


class ConsoleStream(OStream):
    def __init__(self):
        super().__init__()

    def log(self, msg: str):
        print(f"[{datetime.now().strftime("%H:%M:%S")}] {msg}")
