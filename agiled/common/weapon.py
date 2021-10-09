from common.entity import Projectile
from common.item import Item


class Weapon(Item):
    def __init__(self, title, speed, damage):
        super().__init__(title)
        self._speed = speed
        self._damage = damage

    def generate_projectile(self, speed, angle, damage):
        adjusted_speed = \
            (speed[0]*self._speed, speed[1]*self._speed)

        adjusted_damage = self._damage + damage
        return Projectile(adjusted_speed, adjusted_damage, angle)

    def get_effect(self):
        return None

    def __str__(self):
        return "{}\n| Damage: {}\n| Speed: {}".format(self._title, self._damage, self._speed)
