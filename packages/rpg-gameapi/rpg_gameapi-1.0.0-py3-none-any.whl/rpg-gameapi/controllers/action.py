from time import time
from enum import Enum

from rpggameapi.loggers.logger import Logger
from rpggameapi.loggers.streams import OStream, ConsoleStream


class ActionType(Enum):
    ACCOUNT_CREATE = "ACCOUNT_CREATE"
    CHARACTER_CREATE = "CHARACTER_CREATE"
    CHARACTER_DELETE = "CHARACTER_DELETE"
    CURRENCY_ADDED = "CURRENCY_ADDED"
    CURRENCY_REMOVED = "CURRENCY_REMOVED"
    SHOP_ITEM_BUY = "SHOP_ITEM_BUY"
    MAP_CELL_LOAD = "MAP_CELL_LOAD"
    MAP_ENTITIES_LOAD = "MAP_ENTITIES_LOAD"


class ActionStatusType(Enum):
    SUCCESS = "SUCCESS"
    PENDING = "PENDING"
    FAILED = "FAILED"
    ERROR = "ERROR"


class ActionStatus:
    def __init__(self, action_type: ActionStatusType):
        self.__type =  action_type

    @property
    def type(self) -> ActionStatusType:
        return self.__type

    @type.setter
    def type(self, status_type: ActionStatusType):
        self.__type = status_type


class ActionLogger(Logger):
    def __init__(self, stream: OStream):
        super().__init__(stream)

    def log(self, action):
        res_msg = "Action initialized"
        if action.content:
            res_msg = f"Response: {action.status.type.name} | {action.content}"

        self.stream.log(f"(ACTION) {action.type.name} > {res_msg}")


class Action:
    logger = ActionLogger(ConsoleStream())

    def __init__(self, action_type: ActionType, logger = logger):
        self.__type = action_type
        self.__timestamp = time()
        self.__status = ActionStatus(ActionStatusType.PENDING)
        self.__response = None
        self.__content = None
        self.__logger = logger

        if self.__logger:
            logger.log(self)

    @property
    def type(self) -> ActionType:
        return self.__type

    @property
    def status(self) -> ActionStatus:
        return self.__status

    @status.setter
    def status(self, status_type: ActionStatusType):
        self.__status.type = status_type

    @property
    def timestamp(self) -> float:
        return self.__timestamp

    @property
    def content(self):
        return self.__content

    @property
    def has_response(self) -> bool:
        return True if self.__response else False

    def response(self, content = None):
        if self.has_response:
            return self.__response

        self.__response = ActionResponse(self, self.status, content)
        self.__content = self.__response.content
        if self.__logger:
            self.__logger.log(self.__response)

        return self.__response


class ActionResponse:
    def __init__(self, action: Action, status: ActionStatus, content = None):
        self.__action = action
        self.__status = status
        self.__type  =  action.type
        self.__timestamp = time()
        self.__content = content

    @property
    def action(self) -> Action:
        return self.__action

    @property
    def status(self) -> ActionStatus:
        return self.__status

    @property
    def type(self) -> ActionType:
        return self.__type

    @property
    def timestamp(self) -> float:
        return self.__timestamp

    @property
    def content(self):
        return self.__content

