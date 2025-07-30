from time import time

from rpggameapi.containers.inventory import PlayerInventory
from rpggameapi.containers.registry import TradableCurrencyRegistry
from rpggameapi.controllers.action import ActionResponse


class CharacterError(Exception):
    pass


class Character:
    max_name_length = 18

    def __init__(self,
                 account,
                 char_id,
                 name: str,
                 timestamp: float = None,
                 inventory = None,
                 currencies: TradableCurrencyRegistry = None
                 ):
        self.account = account
        self.__char_id = char_id
        self.name = name
        self.__created_ts = timestamp if timestamp else time()
        self.__inventory = inventory if inventory else PlayerInventory(self)
        self.__currencies = currencies if currencies else TradableCurrencyRegistry()

    @property
    def char_id(self):
        return self.__char_id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        if not _is_name_valid(name):
            raise ValueError(
                f"Provided name is invalid or exceeds the {self.max_name_length} character length."
            )

        self.__name = name

    @property
    def created(self) -> float:
        return self.__created_ts

    @property
    def inventory(self):
        return self.__inventory

    @property
    def currencies(self) -> TradableCurrencyRegistry:
        char_currencies = [currency for currency in self.__currencies]
        acc_currencies = [currency for currency in self.account.currencies]

        currencies = TradableCurrencyRegistry()
        for currency in (char_currencies + acc_currencies):
            currencies.add(currency)

        return currencies

    def __str__(self):
        return self.name

    @staticmethod
    def create(account, name: str) -> ActionResponse:
        return account.create_character(name)


def _is_name_valid(name: str) -> bool:
    if not name.strip() or len(name) > Character.max_name_length:
        return False

    return True
