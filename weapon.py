import pygame as pg

from typing import Any


class WeaponSystem(pg.sprite.Sprite):
    def __init__(self, position: pg.Vector2):
        super().__init__()

        self.mount_position = position

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass


class Turret(WeaponSystem):
    def __init__(self, position: pg.Vector2):
        super().__init__(position)

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass


class Bay(WeaponSystem):
    def __init__(self, position: pg.Vector2):
        super().__init__(position)
        pass

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass
