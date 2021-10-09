from common.item import Item

class Inventory():
    """Player Inventory"""

    def __init__(self, inventory: list):
        # Inventory directly model to inventory screen
        # Bottom layer [3][0] to [3][7] is hotbar
        if inventory is None:
            self._inventory = [[[] for x in range(5)] for y in range(2)]
        else:
            self._inventory = inventory
        self._inventory_size = 10
        self._boots = None
        self._weapon = None

    # Getters
    # ----------------------------------------------------------------------
    def get_inventory(self):
        """Return Inventory"""
        return self._inventory
    
    def get_hotbar(self):
        """Returns the hotbar"""
        return self._inventory[len(self._inventory)-1]

    def get_weapon(self) -> None:
        """Get current player weapon
        """
        return self._weapon

    def get_boots(self):
        return self._boots
    # Setters
    # ----------------------------------------------------------------------
    def set_inventory(self, item):
        """Set Inventory"""
        self._inventory = item
    def set_weapon(self, weapon) -> None:
        """Set current player weapon

        Args:
            weapon (Weapon): Player's new weapon
        """
        self._weapon = weapon

    def set_boots(self,boots):
        self._boots = boots
    # Properties
    # ----------------------------------------------------------------------
    inventory = property(get_inventory,set_inventory)
    hotbar = property(get_hotbar)
    weapon = property(get_weapon, set_weapon)
    boots = property(get_boots, set_boots)

    # Methods
    # ----------------------------------------------------------------------
    def add(self, item: Item):
        """Add an item"""
        remove = False
        i,j = self._find_slot(item, remove)
        self._inventory[i][j].append(item)

    def remove(self, item: Item):
        remove = True
        i,j = self._find_slot(item, remove)
        if self._inventory[i][j]:
            self._inventory[i][j].remove(item)
        
    def _find_slot(self, item: Item, remove: bool):
        row_index = 0
        open_row_index = -1
        for row in self._inventory:
            col_index = 0
            open_col_index = len(self._inventory[0])
            for slot in row:
                if slot and (item.stackable or remove) and slot[0] == item:
                    return row_index, col_index
                if not slot:
                    open_col_index = min(col_index, open_col_index)
                    open_row_index = max(row_index, open_row_index)
                col_index += 1
            row_index += 1
        return open_row_index, open_col_index

    def clear_inventory(self):
        """Clear the whole inventory"""
        self._inventory = [[[] for x in range(len(self._inventory[0])-1)] for y in range(len(self._inventory)-1)]
