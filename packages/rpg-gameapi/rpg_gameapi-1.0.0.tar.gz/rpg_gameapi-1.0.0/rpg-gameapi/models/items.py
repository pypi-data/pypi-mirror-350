class Item:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)


class InventoryItem(Item):
    def __init__(self,
                 inv_id,
                 item: Item,
                 obtained_ts: float = None
                 ):
        self.__inv_id = inv_id
        self.__item = item
        self.__obtained = obtained_ts
        super().__init__(**self.__item.__dict__)

    @property
    def inv_id(self):
        return self.__inv_id

    @property
    def item(self) -> Item:
        return self.__item

    @property
    def obtained(self):
        return self.__obtained
