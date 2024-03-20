import pygame as pg

from typing import Any


class WeaponSystem(pg.sprite.Sprite):
    def __init__(self, position: pg.Vector2):
        super().__init__()

        self.mount_position: pg.Vector2 = position
        self.current_position: pg.Vector2 = self.mount_position
        self.rotation_angle: float = 0

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass


class Turret(WeaponSystem):
    def __init__(self, position: pg.Vector2):
        super().__init__(position)

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass

    def rotate(self, angle: float):
        self.rotation_angle = angle
        self.current_position = self.mount_position.rotate(angle)


class Bay(WeaponSystem):
    def __init__(self, position: pg.Vector2):
        super().__init__(position)
        pass

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass
