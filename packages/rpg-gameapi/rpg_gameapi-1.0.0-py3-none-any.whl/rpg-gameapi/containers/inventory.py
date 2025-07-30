from abc import ABC

from rpggameapi.containers.registry import Registry


class Inventory(Registry, ABC):
    def __init__(self, items):
        super().__init__()
        if items:
            self.__add_regitems(items)

    @property
    def items(self):
        return self._items

    def __add_regitems(self, items):
        for item in items:
            self.add(item)

    def __iter__(self):
        return iter(self.items)


class PlayerInventory(Inventory):
    def __init__(self, character, *items):
        self.__character = character
        super().__init__(items)

    @property
    def character(self):
        return self.__character
