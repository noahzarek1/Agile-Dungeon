"""Class which holds the current state of the game"""

import math
from typing import List

import pygame
from pygame.locals import K_w, K_s, K_a, K_d, K_1, K_2, K_3, K_4, K_5

from common import audio
from common.entity import DroppedItem, Player, Enemy, Actor, Boss
from common.potion import Potion, PotionFactory
from common.item import Key
from common.room import Room, SpawnLocations
from common.weapon import Weapon
from common.map_generator import DungeonGenerator
from common.boots import Boots

SCORE_MULTIPLIER = 10

class State:
    """Class which holds the current state of the game"""

    def __init__(self) -> None:
        self._paused = True
        self._started = False

        # The player
        self._player = Player()

        self._player.inventory.add(Key())
        # The list of currently active actors
        self._actors: List[Actor] = []

        # The current room
        self._room = None
        self._root = None
        self._player = None
        self._game_over = False
        self._actors = []
        self._projectiles = []

        # Set the background music
        self._background_music = None
        self.change_background_music(audio.Music.Song.DUNGEON01)

        # Currently active projectiles
        self._projectiles = []
        self._dropped_items = []

        # Number of enemies killed by player
        self._num_dead_enemies = 0

        # Player's current score
        self._score = 0

        self._game_over = False
        self._room_count = 0
        self.spawn()
        self.enter_new_dungeon()

    # Getters
    # ----------------------------------------------------------------------
    def get_room_at_direction(self) -> Room:
        """Get the current room

        Returns:
            Room: The current room
        """
        return self._room

    def get_room_count(self):
        return self._room_count

    def get_actors(self) -> List[Actor]:
        """Get all the current actors

        Returns:
            The current actor group
        """
        return self._actors

    def get_player(self) -> Actor:
        """Returns the player

        Returns:
            The player
        """
        return self._player

    def get_projectiles(self) -> List:
        """Return the currently active projectiles

        Return:
            The currently active projectiles
        """
        return self._projectiles

    def get_score(self) -> int:
        """Return the current score

        Return:
            The current score
        """
        return self._score

    def get_dropped_items(self) -> List:
        return self._dropped_items

    def get_paused(self) -> bool:
        """Return if game is paused"""
        return self._paused

    def get_started(self) -> bool:
        """Return if game is started"""
        return self._started

    # Setters
    # ----------------------------------------------------------------------
    def set_root(self, root: Room) -> None:
        """Set the current root

        Args:
            room (Room): A room object
        """
        self._root = root

    def set_room(self, room: Room) -> None:
        """Set the current room

        Args:
            room (Room): A room object
        """
        self._room = room

    def set_player(self, player: Actor) -> None:
        """Set the player to a new Actor object

        Args:
            player (Actor): A player object
        """
        self._player = player

    def set_paused(self, update: bool) -> None:
        """Set game's pause state"""
        self._paused = update

    def set_started(self, update: bool) -> None:
        """Set if game is started"""
        self._started = update

    def set_score(self, new_score: int) -> None:
        """Set the score

        Args:
            score (int): An int
        """
        self._score = new_score

    # Properties
    # ----------------------------------------------------------------------
    player = property(get_player, set_player)
    actors = property(get_actors)
    room = property(get_room_at_direction, set_room)
    projectiles = property(get_projectiles)
    paused = property(get_paused, set_paused)
    started = property(get_started, set_started)
    score = property(get_score, set_score)

    # Methods
    # ----------------------------------------------------------------------

    def clear_entities(self):
        self._projectiles = []
        self._actors = []
        self._dropped_items = []

    def game_is_over(self):
        return self._game_over

    def enter_new_dungeon(self):
        self.clear_entities()

        map_generator = DungeonGenerator()
        self._root = map_generator.generate_map(None, 5)

        self._room_count += 1
        self.set_room(self._root)

        self._player.set_coords(SpawnLocations.CENTER)

    def spawn(self) -> None:
        """Respawn player"""
        self.set_room(self._root)
        self._room_count = 0
        self.score = 0

        self._player = Player()
        self._player.set_coords(SpawnLocations.CENTER)

        # When the player spawns, give them two health potions
        potion_factory = PotionFactory()
        self._player.inventory.add(potion_factory.get_potion(Potion.PotionType.HEALING, 5))

        self._player.inventory.add(potion_factory.get_potion(Potion.PotionType.HEALING, 5))

        self._player.inventory.add(potion_factory.get_potion(Potion.PotionType.SPEED, 5))

        # Clear active actors and projectiles
        self.clear_entities()

        self._player.inventory.weapon = Weapon(
                                                title="Basic Bow",
                                                speed=8,
                                                damage=20
                                                )
        self._player.inventory.boots = Boots(
                                                title="Cheap Boots",
                                                defense_buff=0,
                                                strength_buff=10,
                                                speed_buff=2
                                            )

        self._game_over = False

        self.change_background_music(audio.Music.Song.DUNGEON01)

    def change_background_music(self, song: audio.Music.Song, loops: int = -1) -> None:
        """Change the background music for the state

        Args:
            song (audio.Music.Song): Song file to play
        """
        if self._background_music != song:
            self._background_music = song
            audio.Music(song, loops).play()

    def update(self) -> None:
        """Updates the game's state"""
        # self.check_important_keys(events)
        if not self._paused:
            self.update_player()
            # update enemy Movement
            for enemy in self.actors:
                enemy.check_for_trigger(self._player)
                if enemy.is_triggered():
                    self.make_enemy_chase(enemy, self._player)
                else:
                    self.move_enemy(enemy)
            self.update_environment()

    def update_player(self):
        # Update the player's movement
        self.move_player()

        # Update the player's status effects
        self._player.update_effects()

        self._player.update_player_attributes()
        # Check user click behavior
        self.check_user_click()

        self.check_item_keys()

    def update_environment(self):
        # Check the tile behavior
        self.check_tile_behavior()

        # Check projectile collision and destroy collided
        # projectiles
        self.check_projectile_collision()

        self.check_dropped_item_collision()

        self.kill_dead_enemies()

        self.update_damage_timers()

        # NOTE: TEMPORARY
        # Check if player is colliding with enemy
        enemies = self.get_enemies_colliding_with_player()
        if enemies and self._player.can_be_damaged():
            self._player.take_damage(enemies[0].attributes.get_current_strength())

        if self._player.is_dead():
            self._game_over = True
            self.paused = True
            self.change_background_music(audio.Music.Song.GAMEOVER, 1)

    def check_item_keys(self):
        """Checks if any item activating keys are pressed
        and uses accordingly"""
        keys = pygame.key.get_pressed()

        key = None

        if keys[K_1]:
            key = 0
        elif keys[K_2]:
            key = 1
        elif keys[K_3]:
            key = 2
        elif keys[K_4]:
            key = 3
        elif keys[K_5]:
            key = 4

        if key is not None:
            self._player.use_item(key)

    # def check_important_keys(self, events):
    #     keys = pygame.key.get_pressed()

    #     if keys[K_i]:
    #         self._inventory_open = not self._inventory_open
    #         self._paused = not self._paused
    #     elif keys[K_p]:
    #         self._paused = not self._paused

    def update_damage_timers(self):
        """Updates the player and actor's damage timers"""
        # If the player's damage timer is not 0, decrement it
        if not self._player.can_be_damaged():
            self._player.update_damage_timer()

        for actor in self._actors:
            actor.update_damage_timer()

    def kill_dead_enemies(self):
        """Kills the dead enemies"""
        for enemy in self._actors:
            # If the enemy is dead, remove it
            if enemy.is_dead():
                new_item = DroppedItem(None)
                new_item.set_coords(enemy.coords)
                self._actors.remove(enemy)
                self._num_dead_enemies += 1
                self._dropped_items.append(new_item)

    def check_dropped_item_collision(self) -> None:
        """Act on dropped item collision"""
        collision = pygame.sprite.spritecollide(self.player,self._dropped_items, False)

        for col in collision:
            self.score += SCORE_MULTIPLIER
            self._dropped_items.remove(col)


    def check_projectile_collision(self) -> None:
        """Act on projectile collision"""

        # Iterate through each projectile and check if it can move
        for proj in self.projectiles:

            # If it cant move, it has collided, so remove it
            if not self.move_entity_if_possible(proj.speed, proj):
                self.projectiles.remove(proj)

            elif proj.is_out_of_range():
                self.projectiles.remove(proj)

        # Check every enemy to see if it has been collided with a sprite
        for enemy in self._actors:
            # Get projectiles that collide with the current enemy
            collision = pygame.sprite.spritecollide(enemy, self.projectiles, False)

            # For each collision
            for col in collision:
                # Take the damage from the enemy's hitpoints
                enemy.take_damage(col.damage)

                # Remove the projectile
                self.projectiles.remove(col)

    def check_user_click(self) -> None:
        """User click behavior"""
        player = self.player

        # If the player's shot timer is not 0, decrement it
        if not player.can_shoot():
            player.shot_timer -= 1

        # Check if MB1 is pressed
        mb1_is_down = pygame.mouse.get_pressed()[0]

        if mb1_is_down:
            if player.can_shoot():
                # Get the player and mouse coordinates
                player_coords = player.coords
                mouse_coords = pygame.mouse.get_pos()

                # We'll  use a little trig to make normalizing
                # the direction vector easier

                # Get the x/y differences (opposite & adjacent)
                adj = mouse_coords[0] - player_coords[0]
                opp = mouse_coords[1] - player_coords[1]

                if adj == opp == 0:
                    opp = 1

                # Compute the hypotenuse
                hyp = math.sqrt(adj * adj + opp * opp)

                # Normalize the directional vector
                # (Basically, turn the mouse x/y into two base vectors)
                # (that can then be multiplied by a speed constant)
                x_speed, y_speed = adj / hyp, opp / hyp

                angle = calculate_mouse_angle(opp, adj)

                # Create a new projectile from player
                new_proj = player.generate_attack((x_speed, y_speed), angle)

                # Add the new projectile to the state
                self.projectiles.append(new_proj)

                # Play bow sound effect
                sound_effect = audio.SoundEffect(audio.SoundEffect.Effect.ARROW)
                sound_effect.play()

    def get_enemies_colliding_with_player(self) -> List[Actor]:
        """Get all the enemies currently colliding with the player

        Returns:
            A list of actors colliding with the player
        """
        # Get all the sprites currently colliding with the player
        return pygame.sprite.spritecollide(self.player, self._actors, False)        

    def initialize_room(self):
        """Initializes the current room"""

        # Iterate through each row
        spawned_boss = False
        for row_index, row in enumerate(self.room.get_sprite_matrix()):
            for col_index, col in enumerate(row.sprites()):
                # If the tile is an enemy spawnpoint, add the enemy
                if col.is_spawnpoint:
                    temp_enemy = Enemy()
                    spawn_x = col_index * 32 + ((32 - temp_enemy.rect.width) / 2)
                    spawn_y = row_index * 32 + ((32 - temp_enemy.rect.height) / 2)
                    temp_enemy.coords = (spawn_x, spawn_y)

                    self._actors.append(temp_enemy)

                if col.is_portal and not spawned_boss:
                    temp_boss = Boss()
                    temp_boss.coords = (col_index * 32, row_index * 32)
                    self._actors.append(temp_boss)
                    spawned_boss = True

        # Set the room to initialized
        self.room.set_initialized(True)

    def move_player(self):
        """Update the player's movement"""

        # Get currently pressed keys
        keys = pygame.key.get_pressed()

        # Change in X/Y coordinate
        x_change, y_change = (0, 0)

        # Check for WSAD pressed and set x/y changes accordingly

        # Check for W or S
        if keys[K_w]:
            y_change = -1 * self._player.get_speed()
        if keys[K_s]:
            y_change = self._player.get_speed()

        # Check for A or D
        if keys[K_a]:
            x_change = -1 * self._player.get_speed()
        if keys[K_d]:
            x_change = self._player.get_speed()

        # If both, stop movement
        if keys[K_s] and keys[K_w]:
            y_change = 0
        if keys[K_a] and keys[K_d]:
            x_change = 0

        # Move the player in changes if available
        if x_change != 0:
            self.move_entity_if_possible([x_change, 0], self.player)
        if y_change != 0:
            self.move_entity_if_possible([0, y_change], self.player)

    def move_enemy(self, enemy: Actor):
        vectors = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, -1], [-1, 1]]

        if enemy.get_distance() <= 0:
            enemy.get_new_direction()

        direction = vectors[enemy.get_direction()]

        if self.entity_can_move(direction, enemy):
            self.move_entity_if_possible(direction, enemy)
            enemy.set_distance(-1)
        else:
            enemy.get_new_direction()

    def make_enemy_chase(self, enemy, player: Actor):
        # Find direction vector (dx, dy) between enemy and player.
        vect = pygame.math.Vector2(player.rect.x - enemy.rect.x, player.rect.y - enemy.rect.y)

        dx = player.rect.x - enemy.rect.x
        dy = player.rect.y - enemy.rect.y
        dist = math.hypot(dx, dy)

        if player.rect.x > enemy.rect.x:
            x = 1
        else:
            x = -1

        if player.rect.y > enemy.rect.y:
            y = 1
        else:
            y = -1

        if dist > 3 and self.entity_can_move([x, y], enemy):
            # Move along this normalized vector towards the player at charging speed enemy cannot share exact
            # coordinates with player
            vect.scale_to_length(enemy.get_charge_speed())
            enemy.rect.move_ip(vect)
        #else:
            #enemy.set_triggered(False)
            #self.move_enemy(enemy)

    def entity_can_move(self, change, entity) -> bool:
        """Check if a move is possible for an entity"""
        # Room matrix
        room_array = self.room.get_sprite_matrix()

        # Get the entities old position
        old_pos = entity.coords

        # Update the player for the frame
        entity.update_position(change)

        # For every row, check for sprite collision between the player and any tile
        for row in room_array:

            # Get all the sprites currently colliding with the player
            for collision in pygame.sprite.spritecollide(entity, row, False):

                # If the colliding sprite isn't passable, set the player's coordinates
                # to their old coordinates before moving
                if not collision.is_passable:
                    entity.coords = old_pos
                    return False

        entity.coords = old_pos
        return True

    def move_entity_if_possible(self, change: tuple, entity: Actor) -> bool:
        """Update the moves the player if possible

        Args:
            change (tuple): x/y values of the entity's change in position
            entity (Actor): Entity to move

        Returns:
            bool: Whether entity was able to move
        """

        # Room matrix
        room_array = self.room.get_sprite_matrix()

        # Get the player's old position
        old_pos = entity.coords

        # Update the player for the frame
        entity.update_position(change)

        # For every row, check for sprite collision between the player and any tile
        for row in room_array:

            # Get all the sprites currently colliding with the player
            for collision in pygame.sprite.spritecollide(entity, row, False):

                # If the colliding sprite isn't passable, set the player's coordinates
                # to their old coordinates before moving
                if not collision.is_passable and (not collision.is_door or self._actors):
                    entity.coords = old_pos
                    return False
                if collision.is_door:
                    return False

        return True

    def check_tile_behavior(self) -> None:
        """Checks for tiles that have behavior"""

        # Room matrix
        room_array = self._room.get_sprite_matrix()

        # Player
        player = self.player

        through_door = False

        # Loop through each row
        for row in room_array:

            # For each colliding tile
            for collision in pygame.sprite.spritecollide(player, row, False):
                # Do behavior if avialable
                if collision.has_behavior:
                    collision.behavior(self)

                if collision.is_damaging and player.can_be_damaged():
                    # Set damage timer to 30 ticks
                    player.take_damage(5)

                if collision.is_door and not through_door:
                    self.send_player_through_door(collision.door_type)
                    through_door = True

                if collision.is_portal and not through_door:
                    if not self._actors:
                        through_door = True
                        self.enter_new_dungeon()

    def send_player_through_door(self, door_type):
        self.traverse_room(door_type)
        self.clear_entities()

        # Initialize the room / enemy spawns
        if not self.room.is_initialized():
            # Initiaize the room
            self.initialize_room()

    def traverse_room(self, door_type):
        spawn_coords = {
            "north": (19.5 * 32, 22 * 32),
            "south": (19.5 * 32, 2 * 32),
            "east": (1 * 32, 11.5 * 32),
            "west": (38 * 32, 11.5 * 32)
        }

        self._player.set_coords(spawn_coords[door_type])

        door_map = {
            "north": self._room.get_room_at_direction('north'),
            "south": self._room.get_room_at_direction('south'),
            "east": self._room.get_room_at_direction('east'),
            "west": self._room.get_room_at_direction('west')
        }

        self._room = door_map[door_type]


def calculate_mouse_angle(opp: float, adj: float) -> float:
    """Calculate angle of the mouse click from the Player using trigonometry

    Args:
        opp (float): Opposite side of the triangle
        adj (float): Adjacent side of the triangle

    Returns:
        float: Angle of the mouse click
    """
    angle = math.degrees(-math.atan2(opp, adj))
    return (angle + 360) % 360
