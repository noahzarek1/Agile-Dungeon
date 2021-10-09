"""Implements the UI overlay that goes on top of the room scene."""
import pygame
import pygame.freetype
from common import util


class HeadsUpDisplay():
    """Class representing a display for the current health, strength, and defense"""
    def __init__(self):
        # Load up UI fonts
        self._font_icon_solid = pygame.freetype.Font(
            util.get_absolute_path_of_asset("other", "fonts", "fa-solid-900.ttf")
            )
        self._font_icon_regular = pygame.freetype.Font(
            util.get_absolute_path_of_asset("other", "fonts", "fa-regular-400.ttf")
            )
        self._font_text = pygame.freetype.Font(
            util.get_absolute_path_of_asset("other", "fonts", "Macondo-Regular.ttf")
            )

    def draw_health(self, window, posx: int, posy: int, current_hit_points: int, max_hit_points: int, hearts: int):
        """Draw the health bar to the HUD

        Args:
            window ([type]): [description]
            posx (int): [description]
            posy (int): [description]
            current_hit_points (int): Current player hitpoints
            max_hit_points (int): Maximum player hitpoints
            hearts (int): Maximum number of hearts to display on screen
        """
        # Draws player health as a row of hearts. Hearts are three-state: full, broken, or empty.
        health_per_heart = max_hit_points / hearts
        health_broken = max_hit_points / 2

        heart_dims = self._font_icon_regular.get_rect("\uf004", size=24)
        heart_offset = heart_dims.x + 30

        # How many hearts do we need?
        full_hearts = (int)(current_hit_points / health_per_heart)
        any_extra = current_hit_points - (full_hearts * health_per_heart)
        empty_hearts = hearts - (full_hearts + (1 if any_extra > 0 else 0))

        # Draw hearts
        for _ in range(full_hearts):
            self._font_icon_solid.render_to(window, (posx, posy), "\uf004", size=24, fgcolor=(255, 23, 40, 255))
            posx += heart_offset

        if any_extra > 0:
            if any_extra > health_broken:
                self._font_icon_solid.render_to(window, (posx, posy), "\uf004", size=24, fgcolor=(255, 23, 40, 255))
            else:
                self._font_icon_solid.render_to(window, (posx, posy), "\uf7a9", size=24, fgcolor=(128, 12, 20, 255))

            posx += heart_offset

        for _ in range(empty_hearts):
            self._font_icon_regular.render_to(window, (posx, posy), "\uf004", size=24, fgcolor=(10, 10, 10, 255))
            posx += heart_offset

    def draw_overlay(self, window, state):
        """Draws the overlay, reading data from State (eventually)"""
        player_atts = state.player.attributes

        self.draw_health(window, 20, 20, player_atts.current_hitpoints, 100, 10)

        self._font_text.render_to(window, (20, 50), "strength " + str(player_atts.current_strength), size=24)
        self._font_text.render_to(window, (20, 80), "defense " + str(player_atts.current_defense), size=24)
        self._font_text.render_to(window, (20, 110), "speed " + str(player_atts.current_speed), size=24)
        self._font_text.render_to(window, (20, 745), "Score: " + str(state.get_score()), size=24)

        self.draw_status_effects(window, state)
        self.draw_inventory(window, state)
        self.draw_weapon_info(window, state)
        self.draw_boot_info(window, state)
        self.draw_floor_count(window, state)

    def draw_status_effects(self, window, state):
        """Draws the currently active status effects"""
        status_effects = state.player.status_effects
        offset = 0

        for effect in status_effects:
            offset += 20
            self._font_text.render_to(window, (1100, offset), str(effect), size=20)

    def draw_inventory(self, window, state):
        """Draws the player's inventory"""
        hotbar = state.player.inventory.hotbar

        offset = 150
        for index, item in enumerate(hotbar):
            offset += 20
            if item:
                self._font_text.render_to(window, (20, offset), "{}: {}".format(index + 1, item[0]), size=20)
            else:
                self._font_text.render_to(window, (20, offset), "{}: {}".format(index + 1, "empty"), size=20)

    def draw_boot_info(self, window, state):
        weapon = state.player.get_boots()
        offset = 325
        self._font_text.render_to(window, (20,offset), str(weapon), size=20)

    def draw_boot_info(self, window, state):
        weapon = state.player.get_boots()
        offset = 325
        self._font_text.render_to(window, (20,offset), str(weapon), size=20)

    def draw_weapon_info(self, window, state):
        weapon = state.player.get_weapon()
        offset = 300
        self._font_text.render_to(window, (20,offset), str(weapon), size=20)

    def draw_floor_count(self, window, state):
        room_count = state.get_room_count()
        self._font_text.render_to(window, (1280/2 - 50, 20), "Floor: " + str(room_count), size=30)
