from time import time
from uuid import uuid4

from rpggameapi.containers.registry import AccountRegistry, CharacterRegistry, TradableCurrencyRegistry
from rpggameapi.controllers.action import ActionResponse, Action, ActionStatusType, ActionType
from rpggameapi.models.character import Character

class Account:
    def __init__(self, email: str, timestamp: float = None, currencies: TradableCurrencyRegistry = None):
        self.email = email
        self.__created_ts = timestamp if timestamp else time()
        self.__characters = CharacterRegistry()
        self.__currencies = currencies if currencies else TradableCurrencyRegistry()

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email: str):
        if not _is_email_valid(email):
            raise ValueError("Provided email is invalid.")

        self.__email = email

    def create_character(self, name: str) -> ActionResponse:
        action = Action(ActionType.CHARACTER_CREATE)

        char = Character(self, str(uuid4()), name, time())
        if self.__characters:
            self.__characters.add(char)

        action.status = ActionStatusType.SUCCESS
        return action.response(char)

    def delete_character(self, char: Character) -> ActionResponse:
        action = Action(ActionType.CHARACTER_DELETE)

        if char not in self.__characters:
            action.status = ActionStatusType.FAILED
            return action.response("No character with this name could be found.")

        self.__characters.delete(char)
        action.status = ActionStatusType.SUCCESS
        return action.response()

    @property
    def characters(self) -> CharacterRegistry:
        return self.__characters

    @property
    def currencies(self) -> TradableCurrencyRegistry:
        return self.__currencies

    @property
    def created(self) -> float:
        return self.__created_ts

    @classmethod
    def create(cls, email: str, registry: AccountRegistry = None):
        account = cls(email)
        if registry:
            registry.add(account)

        return account

    @classmethod
    def delete(cls, account, registry: AccountRegistry) -> int:
        registry.delete(account)
        return 1


def _is_email_valid(email: str) -> bool:
    if not email.strip() or "@" not in email:
        return False

    return True
