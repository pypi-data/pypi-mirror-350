from abc import ABC, abstractmethod

from rpggameapi.loggers.streams import OStream


class Logger(ABC):
    def __init__(self, stream: OStream):
        self.__stream = stream
        pass

    @property
    def stream(self):
        return self.__stream

    @abstractmethod
    def log(self, msg: str):
        pass
