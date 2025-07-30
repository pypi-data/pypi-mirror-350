from abc import ABC

class Interface(ABC):
    def __init__(self, name: str):
        self.name = name

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        if not name.strip():
            raise ValueError("An interface needs a valid name.")

        self.__name = name