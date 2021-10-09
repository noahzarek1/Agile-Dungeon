from enum import Enum
from common.item import Item
from common.status_effect import StatusEffect


class PotionFactory():
    """Base Potion Item Factory"""
    def __init__(self):
        self._id = 0

    def get_potion(self, potion_type: Enum, potency: int):
        """Return the appropraite potion.
        Args:
            potion_type (Enum): The type of potion to create
            potency (int): The potency of the potion to create
        """
        self._id += 1
        if potion_type == Potion.PotionType.HEALING:
            return Potion(potion_type.value, heal, 240, 60, potency, False, self._id)
        elif potion_type == Potion.PotionType.POISON:
            return Potion(potion_type.value, poison, 240, 60, potency, False, self._id)
        elif potion_type == Potion.PotionType.SPEED:
            return Potion(potion_type.value, speed, 240, 240, potency, True, self._id)
        elif potion_type == Potion.PotionType.STRENGTH:
            return Potion(potion_type.value, strength, 240, 240, potency, True, self._id)
        elif potion_type == Potion.PotionType.DEFENSE:
            return Potion(potion_type.value, defense, 240, 240, potency, True, self._id)


class Potion(Item):
    """A Potion item
    Attributes:
        _effect (StatusEffect): The effect to be applied on use
    """
    class PotionType(Enum):
        """Enum representing each type of potion"""
        STRENGTH = "strength"
        POISON = "poison"
        SPEED = "speed"
        DEFENSE = "defense"
        HEALING = "healing"

    def __init__(self, title, action: callable, timing: int, pulse: int, potency: int, temporary: bool, potion_id: int = 1):
        super().__init__(title)
        self._effect = StatusEffect(title, action, timing, pulse, potency, temporary)
        self._has_effect = True
        self._id = potion_id

    # Getters
    # ----------------------------------------------------------------------
    def get_effect(self):
        """Returns the Potion's effect
        Returns:
            _effect (StatusEffect): The Potion's effect
        """
        return self._effect

    # Properties
    # ----------------------------------------------------------------------
    effect = property(get_effect)

    # Methods
    # ----------------------------------------------------------------------
    def __str__(self):
        return str(self._effect) + " " + str(self._effect.potency)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.__dict__ == other.__dict__


# Helper methods used to create potion's Status Effects
def heal(actor, potency, sound_enabled=True):
    """Heals the actor.

    Args:
        actor (Actor): The actor to be effected
        potency (int): The potency of the effect
        sound_enabled (bool): If a sound effect is played when
        heal is applied. True by default
    """
    actor.take_healing(potency, sound_enabled)


def poison(actor, potency, sound_enabled=True):
    """Poisons the actor

    Args:
        actor (Actor): The actor to be effected
        potency (int): The potency of the effect
        sound_enabled (bool): If a sound effect is played when
        poison is applied. True by default
    """
    actor.take_damage(potency, sound_enabled)


def strength(actor, potency, sound_enabled=True):
    """Increases the strength of the actor.

    Args:
        actor (Actor): The actor to be effected
        potency (int): The potency of the effect
        sound_enabled (bool): If a sound effect is played when
        strength is applied. True by default
    """
    actor.effect_strength(potency)


def defense(actor, potency, sound_enabled=True):
    """Increases the defense of the actor.

    Args:
        actor (Actor): The actor to be effected
        potency (int): The potency of the effect
        sound_enabled (bool): If a sound effect is played when
        defense is applied. True by default
    """
    actor.effect_defense(potency)


def speed(actor, potency, sound_enabled=True):
    """Increases the speed of the actor.

    Args:
        actor (Actor): The actor to be effected
        potency (int): The potency of the effect
        sound_enabled (bool): If a sound effect is played when
        speed is applied. True by default
    """
    actor.inc_speed(potency)
