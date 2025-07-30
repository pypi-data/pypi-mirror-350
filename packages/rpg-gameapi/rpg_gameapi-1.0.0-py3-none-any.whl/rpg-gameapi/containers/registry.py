from rpggameapi.models.currency import Currency


class Registry:
    def __init__(self):
        self.__items = []

    @property
    def _items(self) -> iter:
        return iter(self.__items)

    @_items.setter
    def _items(self, items):
        self.__items = items

    def add(self, item):
        self.__items.append(item)

    def delete(self, item):
        self.__items.remove(item)

    def __getitem__(self, index):
        return self.__items[index]

    def __iter__(self) -> iter:
        return iter(self.__items)

    def __len__(self) -> int:
        return len(self.__items)


class AccountRegistry(Registry):
    def __init__(self):
       super().__init__()

    @property
    def accounts(self):
        return self._items


class CharacterRegistry(Registry):
    def __init__(self):
       super().__init__()

    @property
    def characters(self):
        return self._items


class CurrencyRegistry(Registry):
    def __init__(self):
        super().__init__()

    @property
    def currencies(self):
        return self._items

    def get_currency(self, name: str) -> Currency | None:
        for currency in self.currencies:
            if currency.name == name:
                return currency

        return None

class TradableCurrencyRegistry(CurrencyRegistry):
    def __init__(self):
        super().__init__()

    @property
    def currencies(self):
        return self._items

class NpcRegistry(Registry):
    def __init__(self):
        super().__init__()

    @property
    def npcs(self):
        return self._items

class EntityRegistry(Registry):
    def __init__(self):
        super().__init__()

    @property
    def entities(self):
        return self._items