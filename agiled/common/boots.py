from common.item import Item


class Boots(Item):
    "Class Representing Boots"

    def __init__(self, title, defense_buff, strength_buff, speed_buff):
        super().__init__(title)
        self._defense_buff = defense_buff
        self._strength_buff = strength_buff
        self._speed_buff = speed_buff
        self._applied = False

    # Getters
    # ------------------------------------------------------------------
    def get_title(self):
        return self._title

    def get_defense_buff(self):
        return self._defense_buff

    def get_strength_buff(self):
        return self._strength_buff

    def get_speed_buff(self):
        return self._speed_buff

    def get_if_applied(self):
        return self._applied

    def get_effect(self):
        return None

    # Setters
    # ------------------------------------------------------------------
    def set_if_applied(self, value):
        self._applied = value

    # Properties
    # ----------------------------------------------------------------------
    title = property(get_title)
    speed_buff = property(get_speed_buff)
    strength_buff = property(get_strength_buff)
    defense_buff = property(get_defense_buff)
    applied = property(get_if_applied, set_if_applied)

    # Methods
    # -------------------------------------------------------------------
    def __str__(self):
        template = "{}\n|Defense: {}\n|Strength: {}\n|Speed: {}"
        return template.format(self._title, self._defense_buff, self._strength_buff, self._speed_buff)
