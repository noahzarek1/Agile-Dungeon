"""Scene which controls drawing of the game state"""
from typing import List
from enum import Enum
import pygame

from common.room import Room
from common.state import State
from common.hud import HeadsUpDisplay
from common.entity import Actor
from common.menu import Menu


class Scene():
    """Class representing the Scene (window), which is a reflection of the game state

    Attributes:
        tile_size (int): Size of tiles, in pixels
        width (int): Width of the scene, in pixels
        height (int): Height of the scene, in pixels
        window (Surface): pygame surface which represents objects
    """
    def __init__(self, width, height):
        self._tile_size = 32
        self._width = width
        self._height = height
        self._window = pygame.display.set_mode((width, height))
        self._hud = HeadsUpDisplay()
        self._menu = Menu((width, height))

    def get_menu(self) -> Menu:
        """Return the menu object"""
        return self._menu

    menu = property(get_menu)

    def draw_background(self):
        """Fill in the window background with RGB 0,0,255 (blue)"""
        self._window.fill((0, 0, 255))

    def draw_room(self, room: Room):
        """Draw a simple array of squares corresponding to an array

        Args:
            room (Room): The current room
        """

        # Get the 2d array representing the room
        room_array = room.get_sprite_matrix()

        # Calculate the x/y offsets to center the room
        col_offset = (self._width - 40 * self._tile_size) / 2
        row_offset = (self._height - 24 * self._tile_size) / 2

        for row in room_array:
            row.draw(self._window)

        # Draw the sprite for each tile
        for col_index in range(len(room_array[0].sprites())):
            for row_index, row in enumerate(room_array):
                sprite = row.sprites()[col_index]

                sprite.rect = pygame.Rect(
                    (col_offset + col_index * self._tile_size, row_offset + row_index * self._tile_size),
                    (32, 32)
                )

                pygame.Surface.blit(self._window, sprite.image, sprite.rect)

    def draw_player(self, player: Actor):
        """Draw the player to the screen

        Args:
            player (Actor): A player object
        """
        self._window.blit(player.image, player.coords)

    def draw_actors(self, actors: List[Actor]):
        """Draws the currently active Actors
        Args:
            actors (List[Actor]): A group of actors
        """
        for actor in actors:
            self._window.blit(actor.image, actor.coords)

    def draw_dropped_items(self, items: list):
        for item in items:
            self._window.blit(item.image, item.coords)

    def draw_projectiles(self, projectiles: List):
        """Draws the currently active projectiles

        Args:
            projectiles (List[Projectile]): A list of projectiles
        """
        for projectile in projectiles:
            self._window.blit(projectile.image, projectile.coords)

    def draw_menu(self, screen: Enum):
        self._menu.draw_menu(screen)

    def draw_state(self, state: State):
        """Draw a given state

        Args:
            state: State a state object
        """
        if not state.started:
            self._menu.draw_main_menu()
        elif state.game_is_over():
            self._menu.draw_game_over()
        elif state.paused:
            self._menu.draw_pause_menu()
        else:
            # Draw game objects
            self.draw_room(state.room)
            self.draw_player(state.player)
            self.draw_actors(state.actors)
            self.draw_projectiles(state.projectiles)
            self.draw_dropped_items(state.get_dropped_items())
            # Then draw the HUD
            self._hud.draw_overlay(self._window, state)
