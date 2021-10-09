"""Map Generator class and helper functions"""
import random
import os

from common.room import Room
from common.tileset import TileSet
from common import util

TN = TileSet.TileName


class DungeonGenerator:
    """This class helps generate random maps
    for the game.

    Attributes:
        _tile_map (dict): The map of tiles for string conversion
        _room_count (int): The number of rooms spanning from root
        _room_queue (list): The queue of rooms waiting to be worked on
        _root (Room): The root room
    """
    def __init__(self):
        self._tile_matrixes = []

        self._tile_map = {
            "#": TN.WALL,
            "_": TN.FLOOR,
            "@": TN.WALL_TWO,
            "M": TN.MUSHROOM,
            "X": TN.SPIKES,
            "L": TN.LOCK
        }

        self.load_maps()
        self._room_count = 0
        self._room_queue = []
        self._root = None
        self._last_room = None

    def load_root(self):
        with open(util.get_absolute_path_of_asset("other", "maps", "start.map"), "r") as file:
            tile_matrix = self.str_to_tile_matrix(file.read())
            self._root = Room(tile_matrix)

    def generate_endroom(self):
        with open(util.get_absolute_path_of_asset("other", "maps", "end.map"), "r") as file:
            tile_matrix = self.str_to_tile_matrix(file.read())

        return Room(tile_matrix)

    def load_maps(self):
        """Loads in the pregenerated room maps from the map directory"""
        for filename in os.listdir(util.get_absolute_path_of_asset_directory("other", "maps")):
            if filename not in ["start.map", "end.map"]:
                with open(util.get_absolute_path_of_asset("other", "maps", filename), "r") as file:
                    tile_matrix = self.str_to_tile_matrix(file.read())
                    self._tile_matrixes.append(tile_matrix)

    def generate_map(self, seed, count):
        """Generates a random map given a seed and count

        Args:
            seed: A seed for RNG
            count (int): The number of rooms for the map to have

        Returns:
            A randomly generated map
        """

        self.load_root()
        self._last_room = self._root
        # Seed random if necessary
        if seed:
            random.seed(seed)

        # Set the room count
        self._room_count = count

        self._room_queue.append(self._root)

        # Populate the new root
        self.populate_map()

        # Create the end room
        end = self._last_room
        pick = random.choice(end.get_available_directions())
        end.connect_room(self.generate_endroom(), pick)

        # Reset room count and room queue
        self._room_count = 0
        self._room_queue = []

        return self._root

    def random_room(self):
        """Generates a random room from the map list

        Returns:
            A randomly generated room
        """
        tiles = random.choice(self._tile_matrixes)

        room = [row[:] for row in tiles]

        return Room(room)

    def populate_map(self):
        """Recursively populates a given root room with
        spanning rooms"""

        # If all rooms have been added, return
        if self._room_count <= 0:
            return

        # Otherwhise, get the current room from the queue
        current = self._room_queue.pop(0)

        # Get which directions that room will accept a door in
        # and choose a random number of them
        dirs = current.get_available_directions()
        number_to_add = random.randint(1, len(dirs))
        available_dirs = random.sample(dirs, number_to_add)

        # Populate the available directions
        self.populate_available_directions(current, available_dirs)

        # Recurse
        self.populate_map()

    def populate_available_directions(self, room, directions: list):
        # For each randomly chosen direction
        for direction in directions:
            # Decrement the room count and make a new random room
            self._room_count -= 1
            new_room = self.random_room()

            # Return if all rooms have been created
            if self._room_count <= 0:
                return

            # Connect the new room to the current one
            room.connect_room(new_room, direction)

            # Add the new one to the queue
            self._room_queue.append(new_room)
            self._last_room = new_room

    def str_to_tile_matrix(self, room_str: str) -> Room:
        """Converts a string and dictionary of tiles into a room

        Args:
            room_str (str): The string representing the room

        Returns:
            A room made from the tiles
        """
        # Height/width of room
        rows = room_str.strip().split("\n")

        tile_matrix = []

        for row in rows:
            tile_matrix.append([])

            for column in row:
                if self._tile_map.get(column):
                    tile_matrix[-1].append(self._tile_map[column])

        return tile_matrix

    def get_tile_matrixes(self):
        return self._tile_matrixes

    def get_root(self) -> Room:
        """Return root of map tree

        Returns:
            Room: Root node of generated maps
        """
        return self._root
