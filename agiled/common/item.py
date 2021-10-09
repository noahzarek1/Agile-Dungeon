"""Item classes and subclasses"""
from abc import ABC, abstractmethod

class Item(ABC):
    """Class representing an item
    Attributes:
        _has_effect (bool): If the item has an effect
        _title (str): The item's title
    """
    def __init__(self, title, stackable = False, is_equipable = False):
        self._has_effect = False
        self._title = title
        self._stackable = stackable
        self._is_equipable = is_equipable

    # Getters
    # ----------------------------------------------------------------------
    def get_title(self):
        """Returns the title of the object"""
        return self._title
    
    def get_stackable(self) -> bool:
        """Returns whether the item is stackable"""
        return self._stackable
    
    @abstractmethod
    def get_effect(self):
        """A virtual method that needs to be implemented by children"""
        raise NotImplementedError

    # Properties
    # ----------------------------------------------------------------------
    title = property(get_title)
    stackable = property(get_stackable)
    
    # Methods
    # ----------------------------------------------------------------------
    def has_effect(self):
        """Return if the item has an effect
        Returns:
            If the item has an effect
        """
        return self._has_effect

    def __str__(self):
        """Returns a string representation of the item
        Returns:
            A string representation of the item
        """
        return self._title


class Key(Item):
    def __init__(self):
        super().__init__("Dungeon Key")
        self._has_effect = False
    
    def get_effect(self):
        return None
