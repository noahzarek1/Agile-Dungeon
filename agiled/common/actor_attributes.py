""" Contains the attributes needed in order to calculate mechanics such as combat """


class ActorAttributes:
    """Class which holds an Actor's strength, hitpoints, and defense
        Attributes:
        _base_strength: An integer representing the actor's base strength
        _base_hitpoints: An integer representing the actor's base hitpoints
        _base_defense: An integer representing the actor's base defense
        _base_speed: An integer representing the actor's base speed
        _current_strength: An integer representing the actor's current strength
        _current_hitpoints: An integer representing the actor's current hitpoints
        _current_defense: An integer representing the actor's current defense
        _current_speed: An integer representing the actor's current speed
    """
    def __init__(self, defense: int, hitpoints: int, strength: int, speed: int) -> None:
        self._current_defense = self._base_defense = defense
        self._current_hitpoints = self._base_hitpoints = hitpoints
        self._current_strength = self._base_strength = strength
        self._current_speed = self._base_speed = speed

    # Getters
    # ----------------------------------------------------------------------
    def get_base_strength(self) -> int:
        """Return an actor's base strength.
        Returns:
            int: Actor's base strength
        """
        return self._base_strength

    def get_current_strength(self) -> int:
        """Return an actor's current strength.
        Returns:
            int: Actor's current strength
        """
        return self._current_strength

    def get_base_hitpoints(self) -> int:
        """Return an actor's base hitpoints.
        Returns:
            int: Actor's base hitpoints
        """
        return self._base_hitpoints

    def get_current_hitpoints(self) -> int:
        """Return an actor's current hitpoints.
        Returns:
            int: Actor's current hitpoints
        """
        return self._current_hitpoints

    def get_base_defense(self) -> int:
        """Return an actor's base defense.
        Returns:
            int: Actor's base strength
        """
        return self._base_defense

    def get_current_defense(self) -> int:
        """Return an actor's current defense.
        Returns:
            int: Actor's current strength
        """
        return self._current_defense

    def get_base_speed(self) -> int:
        """Return an actor's base speed.
        Returns:
            int: Actor's base speed
        """
        return self._base_speed

    def get_current_speed(self) -> int:
        """Return an actor's current speed.
        Returns:
            int: Actor's current speed
        """
        return self._current_speed

    # Setters
    # ----------------------------------------------------------------------
    def set_base_strength(self, new_strength: int) -> None:
        """Set an actor's base strength.
        Args:
            new_strength (int): Actor's new base strength
        """
        self._base_strength = new_strength

    def set_current_strength(self, new_strength: int) -> None:
        """Set an actor's current strength.
        Args:
            new_strength (int): Actor's new current strength
        """
        self._current_strength = new_strength

    def set_base_hitpoints(self, new_hitpoints: int) -> None:
        """Set an actor's base hitpoints
        Args:
            new_hitpoints (int): Actor's new base hitpoints
        """
        self._base_hitpoints = new_hitpoints

    def set_current_hitpoints(self, new_hitpoints: int) -> None:
        """Set an actor's current hitpoints
        Args:
            new_hitpoints (int): Actor's new current hitpoints
        """
        self._current_hitpoints = new_hitpoints

    def set_base_defense(self, new_defense: int) -> None:
        """Set an actor's base defense
        Args:
            new_defense (int): Actor's new base defense
        """
        self._base_defense = new_defense

    def set_current_defense(self, new_defense: int) -> None:
        """Set an actor's current defense
        Args:
            new_defense (int): Actor's new current defense
        """
        self._current_defense = new_defense

    def set_base_speed(self, new_speed: int) -> None:
        """Set an actor's base speed
        Args:
            new_defense (int): Actor's new base defense
        """
        self._base_speed = new_speed

    def set_current_speed(self, new_speed: int) -> None:
        """Set an actor's current speed
        Args:
            new_defense (int): Actor's new current speed
        """
        self._current_speed = new_speed

    # Properties
    # ----------------------------------------------------------------------
    base_strength = property(get_base_strength, set_base_strength)
    current_strength = property(get_current_strength, set_current_strength)
    base_defense = property(get_base_defense, set_base_defense)
    current_defense = property(get_current_defense, set_current_defense)
    base_hitpoints = property(get_base_hitpoints, set_base_hitpoints)
    current_hitpoints = property(get_current_hitpoints, set_current_hitpoints)
    base_speed = property(get_base_speed, set_base_speed)
    current_speed = property(get_current_speed, set_current_speed)
