"""Class that represents a single room"""
from typing import List
from common.tileset import TileSet
import pygame


class SpawnLocations():
    """Spawn coordinates for each door and center"""
    NORTH = (20*32, 1*32)
    SOUTH = (20*32, 23*32)
    EAST = (38*32, 11*32)
    WEST = (1*32, 11*32)
    CENTER = (20*32, 12*32)


class Room:
    """Class representing a room that the player can move in, interact with,
    and collide with

    Attributes:
        matrix: A 2d matrix representing a room

        _north_room: Room object representing the room's neighbor to the north
        _south_room: Room object representing the room's neighbor to the south
        _east_room: Room object representing the room's neighbor to the east
        _west_room: Room object representing the room's neighbor to the west

        _matrix: A matrix of TileName's to make sprite map generation more efficient
        _sprite_matrix: A matrix of Tile sprites for drawing and collision logic
        _initialized: A boolean representing if the room has been initialized or not
    """

    def __init__(self, matrix):
        self._north_room: 'Room' = None
        self._south_room: 'Room' = None
        self._east_room: 'Room' = None
        self._west_room: 'Room' = None

        self._matrix: TileSet.TileName = matrix
        self._sprite_matrix: List[pygame.sprite.Group] = None
        self._initialized: bool = False
        self.update_sprite_matrix()

    # Getters
    # ----------------------------------------------------------------------
    def is_initialized(self) -> bool:
        """Return the initialization state of the room"""
        return self._initialized

    def get_sprite_matrix(self) -> List[pygame.sprite.Group]:
        """Returns the room's sprite matrix"""
        return self._sprite_matrix

    def get_room_at_direction(self, direction: str) -> 'Room':
        """Returns the room at a direction

        Args:
            direction (str): The direction

        Returns:
            Room: The room located at that direction
        """
        room = None
        if direction == 'north':
            room = self._north_room
        elif direction == 'south':
            room = self._south_room
        elif direction == 'east':
            room = self._east_room
        elif direction == 'west':
            room = self._west_room
        else:
            raise Exception("Invalid room direction: " + direction)

        return room

    # Setters
    # ----------------------------------------------------------------------
    def set_initialized(self, initialized: bool):
        """Set the initialization state of the room

        Args:
            initialized (bool): The initialization state
        """
        self._initialized = initialized

    def set_room(self, direction: str, room: 'Room'):
        """Puts a room at the given direction

        Args:
            direction (str): The direction to set
            room (Room): The room to set
        """
        if direction == 'north':
            self._north_room = room
        elif direction == 'south':
            self._south_room = room
        elif direction == 'east':
            self._east_room = room
        elif direction == 'west':
            self._west_room = room

        else:
            raise Exception("Invalid direction to set: " + direction)

    # Methods
    # ----------------------------------------------------------------------
    def connect_room(self, room_to_add: 'Room', direction: str):
        """Connects a room to its neighbor
        Args:
            room_to_add (Room): Room to connect to the current object.
            direction (str): Direction in which the new room is connected
        """
        if direction not in self.get_available_directions():
            raise Exception("Direction: " + direction + " is already occupied")

        self.set_room(direction, room_to_add)
        self.add_door(direction)

        if direction == 'west':
            room_to_add.set_room('east', self)
            room_to_add.add_door('east')

        elif direction == 'east':
            room_to_add.set_room('west', self)
            room_to_add.add_door('west')

        elif direction == 'north':
            room_to_add.set_room('south', self)
            room_to_add.add_door('south')

        elif direction == 'south':
            room_to_add.set_room('north', self)
            room_to_add.add_door('north')

    def add_door(self, direction: str):
        """Adds a door to the given direction in the sprite matrix

        Args:
            direction (str): The direction to add
        """
        if direction == "north":
            self.set_tile(0, 19, TileSet.TileName.NORTH)
            self.set_tile(0, 20, TileSet.TileName.NORTH)

        elif direction == "south":
            self.set_tile(23, 19, TileSet.TileName.SOUTH)
            self.set_tile(23, 20, TileSet.TileName.SOUTH)

        elif direction == "east":
            self.set_tile(11, 39, TileSet.TileName.EAST)
            self.set_tile(12, 39, TileSet.TileName.EAST)

        elif direction == "west":
            self.set_tile(11, 0, TileSet.TileName.WEST)
            self.set_tile(12, 0, TileSet.TileName.WEST)

        self.update_sprite_matrix()

    def set_tile(self, column: int, row: int, tilename: str):
        """Sets the tile at position (x,y) to the TileName

        Args:
            column (int): The desired column position
            row (int): The desired row position
            tilename (TileName): The desired tile to be set
        """
        self._matrix[column][row] = tilename

    def update_sprite_matrix(self):
        """Converts a tile-name matrix to a sprite matrix"

        Args:
            self._matrix (list[TileName]): Matrix of tile names
        """
        sprite_matrix = []

        tile_set = TileSet()

        for column in range(len(self._matrix)):
            sprite_matrix.append(pygame.sprite.Group())

            for row in range(len(self._matrix[0])):
                sprite_matrix[column].add(
                    tile_set.get_tile(self._matrix[column][row])
                )

        self._sprite_matrix = sprite_matrix

    def get_available_directions(self) -> List[str]:
        """Returns the unoccupied directions for the room

        Returns:
            (List) The unoccupied directions of the room
        """
        possible = ["north", "south", "east", "west"]

        remaining = []

        for direction in possible:
            if self.get_room_at_direction(direction) is None:
                remaining.append(direction)

        return remaining
