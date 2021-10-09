"""Holds the status effect class and some basic effects"""
from typing import Callable


class StatusEffect:
    """This class represents status effects that can be
    applied to an actor like healing or poison.
    Attributes:
        _action (Callable): The action the effect has
        _time: (int): The total time of the effect
        _pulse: (int): The time between effect applications
        _potency: (int): The strength of the effect
        _is_temporary: (bool): If the effect is temporary
    """
    def __init__(self, title: str, action, time: int, pulse: int, potency: int, temporary: int):
        self._title = title
        # The action that the status effect carries out
        self._action = action

        # The total time of the status effect
        self._time = time

        # The time between each application of the effect
        self._pulse = pulse

        # The potency of the effect, has to be positive
        self._potency = abs(potency)

        # Whether or not the effect is temporary, if it's temporary
        # it's effect will be removed once the effect time has elapsed
        self._is_temporary = temporary


    # Getters
    # ----------------------------------------------------------------------
    def get_action(self) -> Callable:
        """Get the StatusEffect's action
        Returns:
            The action
        """
        return self._action

    def get_time(self) -> int:
        """Get the time left on the StatusEffect
        Returns:
            The remaining time for the effect
        """
        return self._time

    def get_potency(self):
        """Returns the Potion's potency
        Returns:
            The Potion's potency
        """
        return self._potency

    def get_is_temporary(self):
        """Returns whether the Potion has a temporary effect
        Returns:
            Whether the potion is temporary
        """
        return self._is_temporary

    # Properties
    # ----------------------------------------------------------------------
    action = property(get_action)
    time = property(get_time)
    potency = property(get_potency)
    is_temporary = property(get_is_temporary)

    # Methods
    # ----------------------------------------------------------------------
    def is_time(self) -> bool:
        """Return if it is time to pulse the effect

        Returns:
            A bool corresponding to if the effect should
            be pulsed
        """
        return self._time % self._pulse == 0

    def update_time(self):
        """Update the current time to the next frame"""
        self._time -= 1

    def has_potency(self) -> bool:
        """Returns true if status effect has a potency.

        If potency is 0 will return false, otherwise true.
        """
        return self._potency

    def __str__(self):
        return "{} {}".format(self._title, self._time)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.__dict__ == other.__dict__
