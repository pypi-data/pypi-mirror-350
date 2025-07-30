from time import time
from rpggameapi.containers.inventory import Inventory
from rpggameapi.controllers.action import ActionResponse, Action, ActionType, ActionStatusType
from rpggameapi.controllers.interface import Interface
from rpggameapi.models.character import Character
from rpggameapi.models.items import InventoryItem, Item
from rpggameapi.models.currency import Currency


class ShopInventory(Inventory):
    def __init__(self, *items):
        super().__init__(items)


class ShopItem(InventoryItem):
    def __init__(self, inv_id, item: Item, currency: Currency = None, price: int | float = 0):
        if not isinstance(item, Item):
            raise ValueError("ShopItems can only be instantiated with Item objects.")

        super().__init__(inv_id, item)
        self.currency = currency
        self.price = price

    @property
    def currency(self):
        return self.__currency

    @currency.setter
    def currency(self, currency: Currency):
        if not isinstance(currency, Currency):
            raise ValueError("Object isn't an instance of a currency.")

        self.__currency = currency

    @property
    def price(self) -> int | float:
        return self.__price

    @price.setter
    def price(self, price: int | float):
        if price < 0:
            raise ValueError("Unsupported negative values in item price.")

        self.__price = price


class Shop(Interface):
    def __init__(self, id, name: str, shop_inventory: ShopInventory = None):
        super().__init__(name)
        self.__id = id
        self.__shop_inventory = shop_inventory if shop_inventory else ShopInventory()

    @property
    def id(self):
        return self.__id

    @property
    def inventory(self) -> ShopInventory:
        return self.__shop_inventory

    @property
    def items(self):
        return iter(self.inventory.items)

    def buy_item(self, character: Character, shop_item: ShopItem) -> ActionResponse:
        action = Action(ActionType.SHOP_ITEM_BUY)

        if not shop_item in self.inventory:
            action.status = ActionStatusType.ERROR
            return action.response(
                "No item was found within the shops inventory registry."
            )

        if not self._can_buy(character, shop_item):
            action.status = ActionStatusType.FAILED
            return action.response(
                "Character didn't have enough of the currency to purchase this item."
            )

        char_item = InventoryItem(
            len(character.inventory) + 1, shop_item.item, time()
        )

        character.currencies.get_currency(shop_item.currency.name).remove(shop_item.price)
        character.inventory.add(char_item)

        action.status = ActionStatusType.SUCCESS
        return action.response(char_item)

    @staticmethod
    def _can_buy(character: Character, shop_item: ShopItem) -> bool:
        char_currency = character.currencies.get_currency(shop_item.currency.name)
        if not character.inventory:
            return False

        if not char_currency or not char_currency.can_afford(shop_item.price):
            return False
        
        return True

    def __iter__(self):
        return self.items
