"""This module holds all the classes for Entity and its related subtypes"""
import math
import random
from enum import Enum

import pygame

from common.actor_attributes import ActorAttributes
from common.item import Item
from common.inventory import Inventory
from common.status_effect import StatusEffect
from common.boots import Boots
from common import audio, util


class EntityType(Enum):
    """ Enum representing each entity_type of an actor """
    PLAYER = "player"
    ENEMY = ["enemy{}".format(i) for i in range(1, 5)]
    BOSS = "boss"
    ITEM = "item"
    OTHER = None


class Entity(pygame.sprite.Sprite):
    """This class represents an entity in the game.
    An entity is defined as something in the game that both
    moves and collides

    Attributes:
        image (Surface): The sprite's image
        rect  (Rect): The sprite's rect
    """
    def __init__(self, entity_type: EntityType) -> None:
        pygame.sprite.Sprite.__init__(self)
        self._entity_type = entity_type

        if entity_type is EntityType.ENEMY:
            choice = random.choice(entity_type.value)
            img_path = util.get_absolute_path_of_asset("images", "sprites", choice + ".png")

            self._image = pygame.image.load(img_path)
            self._rect = pygame.Rect((64, 64), self.image.get_rect().size)

        elif entity_type != EntityType.OTHER:
            img_path = util.get_absolute_path_of_asset("images", "sprites", entity_type.value + ".png")

            self._image = pygame.image.load(img_path)
            self._rect = pygame.Rect((64, 64), self.image.get_rect().size)

    # Getters
    # ----------------------------------------------------------------------
    def get_image(self) -> pygame.Surface:
        """Returns the entity's image

        Return:
            pygame.Surface: The entity's image
        """
        return self._image

    def get_rect(self) -> pygame.Rect:
        """Returns the Sprite's rect

        Return:
            rect: The rect object representing the entity's borders
        """
        return self._rect

    def get_coords(self) -> tuple:
        """Return the coordinates of the Actor's sprite

        Returns:
            tuple: (x, y) coordinates of the sprite's coordinates
        """
        return (self._rect.x, self._rect.y)

    # Setters
    # ----------------------------------------------------------------------
    def set_coords(self, coords: tuple) -> None:
        """Set the x/y coords of the actor

        Args:
            coords (tuple): The x/y coords
        """
        self._rect.x = coords[0]
        self._rect.y = coords[1]

    # Properties
    # ----------------------------------------------------------------------
    coords = property(get_coords, set_coords)
    rect = property(get_rect)
    image = property(get_image)

    # Methods
    # ----------------------------------------------------------------------
    def update_position(self, speed: tuple) -> None:
        """Update the position of the Actor's sprite
        Args:
            speed (tuple): x/y speed values
        """
        self.rect.x += speed[0]
        self.rect.y += speed[1]


# ----------------------------------------------------------------------- #
class Actor(Entity):
    """This class represents an Actor. Something
    That moves either by player control or AI.

    Attributes:
        damage_timer (int): The damage timer
        attributes (ActorAttributes): Attributes for the actor
        status_effects (list[Status_Effect]): List of status effect
        dead (bool): If the actor is dead or not
        damage_delta (int): The time between damage taking
    """
    def __init__(self, entity_type) -> None:
        super().__init__(entity_type)
        self._damage_timer = 0
        self._damage_delta = 0
        self._attributes = None
        self._status_effects = []
        self._dead = False
        self._damage_sound = None

    # Getters
    # ----------------------------------------------------------------------
    def get_attributes(self) -> ActorAttributes:
        """Return the Actor's attributes

        Returns:
            ActorAttributes: The actor's attributes
        """
        return self._attributes

    def get_status_effects(self) -> list:
        """Return an Actor's status effects list

        Returns:
            list: List of the Actor's status effects
        """
        return self._status_effects

    def get_damage_timer(self) -> int:
        """Returns the Actor's damage timer

        Returns:
            the actor's damage timer
        """
        return self._damage_timer

    # Setters
    # ----------------------------------------------------------------------
    def set_damage_timer(self, new_damage_timer):
        """sets the Actor's damage timer"""
        self._damage_timer = new_damage_timer

    # Properties
    # ----------------------------------------------------------------------
    attributes = property(get_attributes)
    damage_timer = property(get_damage_timer, set_damage_timer)
    status_effects = property(get_status_effects)

    # Methods
    # ----------------------------------------------------------------------
    def take_damage(self, damage: int, sound_enabled=True) -> None:
        """Causes the Actor to take damage

        Args:
            damage (int): The damage to be taken
        """
        if self.can_be_damaged():
            damage_done = damage - self._attributes.current_defense
            damage_done = max(1, damage_done)

            self._attributes.current_hitpoints -= damage_done
            self._damage_timer = self._damage_delta

            if self._attributes.current_hitpoints <= 0:
                self._dead = True

            if sound_enabled:
                sound_effect = audio.SoundEffect(audio.SoundEffect.Effect.PAIN01)
                sound_effect.play()

    def take_healing(self, amount: int, sound_enabled=True) -> None:
        """Heals an entity by an amount

        Args:
            amount (int): The amount to be healed
        """
        if self._attributes.current_hitpoints < 100:
            amount = min(amount, 100 - self._attributes.current_hitpoints)
            self._attributes.current_hitpoints += amount

            if sound_enabled:
                sound_effect = audio.SoundEffect(audio.SoundEffect.Effect.HEAL01)
                sound_effect.play()

    def inc_speed(self, amount):
        self.attributes.current_speed += amount

    def effect_strength(self, amount):
        """Increase strength of an entity by an amount

        Args:
            amount (int): The amount to increase strength by
        """
        self.attributes.current_strength += amount

        self.attributes.current_strength = min(self.attributes.current_strength, 100)

    def effect_defense(self, amount):
        """Increase defense of an entity by an amount

        Args:
            amount (int): The amount to increase defense by
        """
        self.attributes.current_defense += amount

        self.attributes.current_defense = min(self.attributes.current_defense, 100)

    def is_dead(self) -> bool:
        """Checks if the Actor is dead

        Returns:
            bool: If the actor is dead
        """
        return self._dead

    def update_effects(self, sound_enabled=True) -> None:
        """Updates the Actor's status effects"""
        for effect in self._status_effects:
            self.apply_status_effect(effect, sound_enabled)

            effect.update_time()

            if effect.get_time() <= 0:
                self._status_effects.remove(effect)
                if effect.is_temporary:
                    self.remove_status_effect(effect)

    def add_status_effect(self, effect: StatusEffect) -> None:
        """Add a new status effect

        Args:
            effect (StatusEffect): A new status effect
        """
        self._status_effects.append(effect)

    def apply_status_effect(self, effect, sound_enabled=True) -> None:
        """Apply the effect of a status effect"""
        # If it is time to apply the status effect
        if effect.is_time():
            # Get the action and apply it
            action = effect.get_action()
            action(self, effect.potency, sound_enabled)

    def remove_status_effect(self, effect):
        """Remove the effect of a status effect.

        Used for temporary effects (ex. strength, speed, defense)
        """
        # Get the action and reverse it
        action = effect.get_action()
        if effect.has_potency():
            action(self, -effect.potency)
        else:
            action(self)

    def update_damage_timer(self) -> None:
        """Update the damage timer"""
        self._damage_timer -= 1

    def can_be_damaged(self) -> bool:
        """Return if the actor can be damaged

        Returns:
            bool: If the actor can be damaged
        """
        if self._attributes is None:
            return False
        return self._damage_timer <= 0


# ----------------------------------------------------------------------- #
class Player(Actor):
    """Class representing a player

    Attributes:
        shot_timer (int): The player's shot timer
    """
    def __init__(self):
        super().__init__(EntityType.PLAYER)
        self._shot_timer = 0
        self._damage_delta = 30
        self._inventory = Inventory(None)
        self._attributes = ActorAttributes(0, 100, 50, 4)

    # Getters
    # ----------------------------------------------------------------------
    def get_shot_timer(self) -> int:
        """Return the current shot timer

        Returns:
            int: Shot timer value
        """
        return self._shot_timer

    def get_speed(self) -> int:

        return self._attributes._current_speed

    def get_attributes(self) -> ActorAttributes:
        """Return the Player's attributes

        Returns:
            ActorAttributes: The player's attributes
        """
        return self._attributes

    def get_inventory(self) -> Inventory:
        """Return the player's inventory

        Returns:
            list: The player's inventory
        """
        return self._inventory

    def get_weapon(self):
        """Return the player's weapon

        Returns:
            Weapon: The player's weapon
        """
        return self._inventory.weapon

    def get_boots(self):
        return self._inventory.boots

    # Setters
    # ----------------------------------------------------------------------
    def set_shot_timer(self, new_shot_timer: int) -> None:
        """Set the shot timer to limit how often the player can shoot

        Args:
            new_shot_timer (int): Shot timer in seconds
        """
        self._shot_timer = new_shot_timer

    def set_weapon(self, weapon) -> None:
        """Set current player weapon

        Args:
            weapon (Weapon): Player's new weapon
        """
        self._inventory.weapon = weapon

    def set_boots(self, boots):
        self._inventory.boots = boots

    def set_inventory(self, value) -> None:
        """Set the players inventory"""
        self._inventory = value

    # Properties
    # ----------------------------------------------------------------------
    shot_timer = property(get_shot_timer, set_shot_timer)
    attributes = property(get_attributes)
    inventory = property(get_inventory, set_inventory)

    # Methods
    # ----------------------------------------------------------------------
    def generate_attack(self, direction: tuple, angle: float) -> 'Projectile':
        """Create a projectile and return it

        Args:
            direction (tuple): Direction to send the projectile

        Returns:
            Projectile: A newly created projectile
        """

        # Set relative position
        proj = self._inventory.weapon.generate_projectile(direction, angle, self._attributes.current_strength)
        proj.coords = self.coords
        self._shot_timer = 15

        return proj

    def update_player_attributes(self):
        if self._inventory.boots.applied is False:
            new_base_strength = self._inventory.boots.strength_buff + self.attributes.current_strength
            new_base_defense = self._inventory.boots.defense_buff  + self.attributes.current_defense
            new_base_speed = self._inventory.boots.speed_buff + self.attributes.current_speed
            self.attributes.current_defense = new_base_defense
            self.attributes.current_strength = new_base_strength
            self.attributes.current_speed = new_base_speed
            self._inventory.boots.applied = True

    def use_item(self, index):
        """Use the item at a given index
        Args:
            index (int): The index
        """
        if self._inventory.hotbar[index]:
            item = self._inventory.hotbar[index][0]
        else:
            return

        if item.has_effect():
            self.add_status_effect(item.get_effect())
            self._inventory.remove(item)

    def can_shoot(self) -> bool:
        """Return if the Player can shoot

        Returns:
            bool: If the player can shoot
        """
        return self._shot_timer <= 0

    def decrease_shot_timer(self, delta=1):
        """Decrease the shot timer

        Args:
            delta (int, optional): Amount to decrease the shot timer. Defaults to 1.
        """
        self._shot_timer -= delta


class Enemy(Actor):
    """Class representing an Enemy"""
    def __init__(self, species=EntityType.ENEMY):
        super().__init__(species)
        self._damage_delta = 5
        self._attributes = ActorAttributes(10, 100, 10, 4)
        self._distance = 128
        self._direction = random.randrange(8)
        self._triggered = False
        self._charge_speed = 3
        self._trigger_range = 110

    def is_triggered(self):
        return self._triggered

    def set_triggered(self, triggered):
        self._triggered = triggered

    def set_distance(self, update_distance):
        self._distance += update_distance

    def get_direction(self):
        return self._direction

    def get_distance(self):
        return self._distance

    def set_direction(self, new_direction):
        self._direction = new_direction

    def get_charge_speed(self):
        return self._charge_speed

    def get_new_direction(self):
        """ sets new direction for enemy to follow 1 is down 2 is up
        3 is right 4 is left also resets distance to 4 tiles"""
        select_move = random.randrange(8)
        self.set_direction(select_move)
        self._distance = 256

    def check_for_trigger(self, player: Actor):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        if dist <= self._trigger_range:
            self._triggered = True
        else:
            self._triggered = False


class Boss(Enemy):
    def __init__(self):
        super().__init__(EntityType.BOSS)
        self._damage_delta = 2
        self._attributes = ActorAttributes(10, 1000, 30,4)
        self._image = pygame.transform.scale(self.image, (64, 64))
        self._rect = self._rect = pygame.Rect((64, 64), self.image.get_rect().size)
        self._trigger_range = 300
        self._charge_speed = 4


class Projectile(Entity):
    """Class representing a Projectile

    Args:
        speed (tuple): A normalized direction vector
        damage (int): The damage the projectile will do

    Attributes:
        _speed (tuple): The speed of the projectile
        _damage (int): The damage of the projectile
        _range (int): The range of the projectile
    """
    def __init__(self, speed: tuple, damage: int, angle: float) -> None:
        super().__init__(EntityType.OTHER)

        self._speed = speed
        self._damage = damage
        self._angle = angle

        # Range is n blocks * tile_size
        # This projectile travels 10 blocks
        self._range = 10*32

        # The projectile's image is currently a green square
        img_path = util.get_absolute_path_of_asset("images", "tiles", "arrow.png")
        self._original_image = pygame.image.load(img_path)
        self._image = pygame.transform.rotate(self._original_image, angle)
        self._rect = self._image.get_rect()

    # Getters
    # ----------------------------------------------------------------------
    def get_speed(self) -> tuple:
        """Return the projectile's speed

        Returns:
            tuple: The projectile's speed
        """
        return self._speed

    def get_damage(self) -> int:
        """Return the projectile's damage

        Returns:
            int: The projectile's damage
        """
        return self._damage

    # Properties
    # ----------------------------------------------------------------------
    speed = property(get_speed)
    damage = property(get_damage)

    # Methods
    # ----------------------------------------------------------------------
    def is_out_of_range(self) -> bool:
        """Returns if the projectile is out of range

        Returns:
            bool: If the projectile is out of range
        """
        return self._range <= 0

    def update_position(self, speed: tuple) -> None:
        """Updates the projectile's position

        Args:
            change (tuple): The change in x/y coordinate

        """
        self._rect.x += speed[0]
        self._rect.y += speed[1]

        self._range -= math.sqrt(pow(speed[0], 2) + pow(speed[1], 2))
        self._range = max(self._range, 0)


class DroppedItem(Entity):
    def __init__(self, item):
        super().__init__(EntityType.ITEM)
        self._item = item

    def get_item(self) -> Item:
        """Return the dropped item's internal Item

        Returns:
            Item: The item within the DroppedItem entity
        """
        return self._item
