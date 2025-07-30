from abc import ABC, abstractmethod

from rpggameapi.containers.registry import EntityRegistry
from rpggameapi.controllers.action import ActionResponse, Action, ActionType, ActionStatusType
from rpggameapi.models.map import Map, MapCell
from rpggameapi.models.entity import NPC
from rpggameapi.models.npc import NpcData


class Instance(ABC):
    def __init__(self, source):
        self.__source = source

    @property
    def source(self):
        return self.__source

    @abstractmethod
    def kill(self):
        pass


class MapCellInstance(Instance):
    def __init__(self, map_cell: MapCell):
        super().__init__(map_cell)
        self.__entities = EntityRegistry()
        self.init_entities()

    @property
    def cell(self) -> MapCell:
        return self.source

    @property
    def entities(self) -> EntityRegistry:
        return self.__entities

    def init_entities(self) -> ActionResponse:
        action = Action(ActionType.MAP_ENTITIES_LOAD)

        if not self.cell.npcs:
            action.status = ActionStatusType.FAILED
            return action.response("There were no initial entities to load.")

        for npcdata in self.cell.npcs:
            if not isinstance(npcdata, NpcData):
                continue

            self.entities.add(
                NPC(len(self.entities) + 1, npcdata)
            )

        action.status = ActionStatusType.SUCCESS
        return action.response()

    def kill(self):
        pass


class MapInstance(Instance):
    def __init__(self, map: Map):
        super().__init__(map)
        self.__active_cell = None

        if map.map_cells:
            self.load_cell(map.map_cells[0])

    @property
    def map(self) -> Map:
        return self.source

    def load_cell(self, map_cell: MapCell | None) -> ActionResponse:
        action = Action(ActionType.MAP_CELL_LOAD)

        if not map_cell:
            action.status = ActionStatusType.ERROR
            return action.response("There was no map cell to load from.")

        cell_instance = MapCellInstance(map_cell)
        self.__active_cell = cell_instance

        action.status = ActionStatusType.SUCCESS
        return action.response(cell_instance)

    @property
    def active_cell(self) -> MapCellInstance:
        return self.__active_cell

    def kill(self):
        pass