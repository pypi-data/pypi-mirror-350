class NpcData:
    def __init__(self, **kwargs):
        for key, value in kwargs.values():
            self.__setattr__(key, value)