import json
from uuid import uuid4
from pathlib import Path

from models.account import Account
from models.currency import Currency
from models.items import InventoryItem, Item
from models.map import Map
from models.shop import Shop, ShopItem

if __name__ == "__main__":
    # Creates a user account with an example email.
    # This will be replaced in the near future to a proper auth service.
    account = Account(email="example@email.com")
    char = account.create_character(name="Frexel").content

    # Create items from a json string of items.
    items_json = json.loads(Path("sample_items.json").read_text())
    items = [Item(**item) for item in items_json]

    # Creating a currency which the shop uses to handle item purchases.
    shop_currency = Currency("Gold", "g")

    # Converts an item into a shop item.
    shop_item = ShopItem(
        inv_id=1,
        item=items[0],
        currency=shop_currency,
        price=200
    )

    # Example of a shop, with an inventory and items for sale.
    shop = Shop(id=str(uuid4()), name="Weapon Shop")

    # Adds a ShopItem to the shop's inventory
    shop.inventory.add(shop_item)
    shop.buy_item(char, shop_item)
