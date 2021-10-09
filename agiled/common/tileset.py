"""Contains the TileSet and Tile classes"""
from enum import Enum
import pygame
from common import util


class Tile(pygame.sprite.Sprite):
    """Class representing a single room tile

    Args:
        img_name (str): The image's name
    Attributes:
        image (surface): The surface holding the Sprite
    """
    def __init__(self, img_name: str):
        super().__init__()
        self.img_path = img_name
        self.image = pygame.image.load(self.img_path)
        self.rect = self.image.get_rect()

        # This should probably be a dict or like TileAttributes or something
        self._is_passable = True
        self._has_behavior = False
        self._is_spawnpoint = False
        self._is_damaging = False
        self._behavior = None
        self._is_door = False
        self._door_type = None
        self._is_portal = False

    # Getters
    # ----------------------------------------------------------------------
    def get_is_door(self):
        return self._is_door

    def get_is_portal(self):
        return self._is_portal

    def get_door_type(self):
        return self._door_type

    def get_is_passable(self):
        """Returns whether the tile is passable or not

        Returns:
            Whether the tile is passable or not
        """
        return self._is_passable

    def get_is_spawnpoint(self):
        """Returns whether the tile is a spawnpoint or not

        Returns:
            Whether the tile is an enemy spawnpoint or not
        """
        return self._is_spawnpoint

    def get_has_behavior(self):
        """Returns whether the tile has behavior or not

        Returns:
            Whether the tile has behavior or not
        """
        return self._has_behavior

    def get_behavior(self):
        """Returns the tile's behavior

        Returns:
            The tile's behavior
        """
        return self._behavior

    def get_is_damaging(self) -> bool:
        """Returns whether the tile damages the player

        Returns:
            bool: Whether the tile damages the player
        """
        return self._is_damaging

    # Setters
    # ----------------------------------------------------------------------
    def set_is_door(self, value: bool) -> None:
        """Set _is_door boolean for tile

        Args:
            value (bool): True/False if tile is a door
        """
        self._is_door = value

    def set_door_type(self, direction: str) -> None:
        """Set _door_type field for tile

        Args:
            direction (str): North/South/East/West direction that door will be placed
        """
        self._door_type = direction

    def set_is_portal(self, value: bool) -> None:
        """Set _is_portal boolean for tile

        Args:
            value (bool): True/False if tile is a portal
        """
        self._is_portal = value

    def set_is_passable(self, value: bool):
        """Set whether the tile is passable or not"""
        self._is_passable = value

    def set_is_spawnpoint(self, value: bool):
        """Set whether the tile is a spawnpoint or not"""
        self._is_spawnpoint = value

    def set_has_behavior(self, value: bool):
        """Set whether the tile has behavior or not"""
        self._has_behavior = value

    def set_behavior(self, value):
        """Sets the tile's behavior"""
        self._behavior = value

    def set_is_damaging(self, value: bool):
        """Set whether the tile damages the player"""
        self._is_damaging = value

    # Properties
    # ----------------------------------------------------------------------
    is_passable = property(get_is_passable, set_is_passable)
    has_behavior = property(get_has_behavior, set_has_behavior)
    is_spawnpoint = property(get_is_spawnpoint, set_is_spawnpoint)
    is_damaging = property(get_is_damaging, set_is_damaging)
    is_door = property(get_is_door, set_is_door)
    is_portal = property(get_is_portal, set_is_portal)
    behavior = property(get_behavior, set_behavior)

    # Methods
    # ----------------------------------------------------------------------
    def copy(self):
        """Copies over a tile to a new tile"""
        ret_t = Tile(self.img_path)
        ret_t.__dict__ = self.__dict__.copy()
        return ret_t


class TileSet:
    """Class representing a tileset for the room

    Attributes:
        TileName(enum): Holds the tilenames and their locations
    """
    class TileName(Enum):
        """Enum class representing tile names"""
        WALL = "wall.png"
        WALL_TWO = "wall-two.png"
        FLOOR = "floor.png"
        SPIKES = "spikes.png"
        MUSHROOM = "mushroom-floor.png"
        NORTH = "door-north.png"
        EAST = "door-east.png"
        SOUTH = "door-south.png"
        WEST = "door-west.png"
        LOCK = "lock.png"

    def __init__(self):
        """Initializes the Tile dictionary"""
        self.tiles = {}
        for _, path in TileSet.TileName.__members__.items():
            img_path = util.get_absolute_path_of_asset("images", "tiles", path.value)
            self.tiles[path] = Tile(img_path)

        self.init_behavior()

    def get_tile(self, name: 'TileSet.TileName') -> Tile:
        """Returns a copy of a tile"""
        return self.tiles[name].copy()

    def init_behavior(self):
        # Later on, this information would be done in its own place, this only exists here for testing
        self.tiles[self.TileName.WALL].is_passable = False
        self.tiles[self.TileName.WALL_TWO].is_passable = False
        self.tiles[self.TileName.NORTH].is_passable = False
        self.tiles[self.TileName.EAST].is_passable = False
        self.tiles[self.TileName.SOUTH].is_passable = False
        self.tiles[self.TileName.WEST].is_passable = False

        self.tiles[self.TileName.MUSHROOM].is_spawnpoint = True
        self.tiles[self.TileName.SPIKES].is_damaging = True

        self.tiles[self.TileName.NORTH].is_door = True
        self.tiles[self.TileName.SOUTH].is_door = True
        self.tiles[self.TileName.EAST].is_door = True
        self.tiles[self.TileName.WEST].is_door = True

        self.tiles[self.TileName.NORTH].door_type = "north"
        self.tiles[self.TileName.SOUTH].door_type = "south"
        self.tiles[self.TileName.EAST].door_type = "east"
        self.tiles[self.TileName.WEST].door_type = "west"

        self.tiles[self.TileName.LOCK].is_passable = True
        self.tiles[self.TileName.LOCK].is_portal = True
