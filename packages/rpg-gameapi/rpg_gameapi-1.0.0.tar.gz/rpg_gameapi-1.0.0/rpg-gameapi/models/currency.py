from rpggameapi.controllers.action import ActionResponse, Action, ActionType, ActionStatusType


class Currency:
    def __init__(self, name: str, ending_char: str = ""):
        self.name = name
        self.__ending_char = ending_char

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        if not name.strip():
            raise ValueError("Currency needs a valid name.")

        self.__name = name

    @property
    def ending_char(self) -> str:
        return self.__ending_char


class TradableCurrency(Currency):
    def __init__(self, currency: Currency, balance: int | float = 0):
        super().__init__(currency.name, currency.ending_char)
        self.balance = balance
    
    @property
    def balance(self) -> int | float:
        return self.__balance

    @balance.setter
    def balance(self, balance: int | float):
        if balance < 0:
            raise ValueError("Unsupported negative values in currency balance.")

        self.__balance = balance

    def add(self, value: int | float) -> ActionResponse:
        action = Action(ActionType.CURRENCY_ADDED)
        self.balance += value

        action.status = ActionStatusType.SUCCESS
        return action.response(self.balance)

    def remove(self, value: int | float) -> ActionResponse:
        action = Action(ActionType.CURRENCY_REMOVED)
        self.balance -= value

        action.status = ActionStatusType.SUCCESS
        return action.response(self.balance)

    def can_afford(self, balance: int | float) -> bool:
        if self.balance < balance:
            return False

        return True

    @property
    def name_char(self) -> str:
        return f"{self.balance}{self.ending_char}"
