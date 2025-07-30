from rpggameapi.containers.registry import Registry, NpcRegistry


class MapRegistry(Registry):
    def __init__(self):
        super().__init__()


class MapCellRegistry(Registry):
    def __init__(self):
        super().__init__()

    @property
    def cells(self) -> iter:
        return iter(self._items)


class Map:
    def __init__(self, id, name: str, map_cells = MapCellRegistry()):
        self.__id = id
        self.name = name
        self.__map_cells = map_cells

    @property
    def map_cells(self):
        return self.__map_cells

    def get_cell(self, id):
        for cell in self.map_cells.cells:
            if cell.id == id:
                return cell

        return None


class MapCell:
    def __init__(self, map: Map, name: str, cell_index: int, npcs = NpcRegistry()):
        self.__map = map
        self.__name = name
        self.__cell_index = cell_index
        self.__npcs = npcs

    @property
    def map(self) -> Map:
        return self.__map

    @property
    def name(self) -> str:
        return self.__name

    @property
    def cell_index(self) -> int:
        return self.cell_index

    @property
    def npcs(self) -> NpcRegistry:
        return self.__npcs
