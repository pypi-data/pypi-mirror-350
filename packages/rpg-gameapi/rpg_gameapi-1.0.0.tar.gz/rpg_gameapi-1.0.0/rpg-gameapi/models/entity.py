from rpggameapi.models.character import Character
from rpggameapi.models.npc import NpcData


class Entity:
    def __init__(self, entity_id, parent_id, name: str, entity_type = None):
        self.__entity_id = entity_id
        self.__parent_id = parent_id
        self.name = name
        self.entity_type = entity_type

    @property
    def entity_id(self):
        return self.__entity_id

    @property
    def parent_id(self):
        return self.__parent_id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def entity_type(self):
        return self.__entity_type

    @entity_type.setter
    def entity_type(self, entity_type):
        self.__entity_type = entity_type


class Player(Entity):
    def __init__(self, character: Character, name: str):
        super().__init__(character.char_id, character.char_id, name)


class NPC(Entity):
    def __init__(self, entity_id, npcdata: NpcData):
        super().__init__(entity_id, npcdata.npc_id, npcdata.name)
