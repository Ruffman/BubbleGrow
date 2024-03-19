from typing import Any
from abc import ABC, abstractmethod

import pygame as pg

from game_internal import TYPE


class Munition(ABC, pg.sprite.Sprite):
    @abstractmethod
    def update(self, *args: Any, **kwargs: Any) -> None:
        pass


class Projectile(Munition):
    def __init__(self, position: pg.Vector2, direction: pg.Vector2, p_type: str):
        super().__init__()

        self.proj_data = TYPE[p_type]['projectile']
        self.image = pg.image.load(self.proj_data['image']).convert()
        self.image = pg.transform.scale(self.image, (self.proj_data['size'], self.proj_data['size']))

        self.rect = self.image.get_rect()
        self.rect.center = position

        self.speed = 1000
        self.direction = direction

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.center = self.rect.center + self.direction * self.speed * kwargs["dt"]


class Beam(Munition):
    def __init__(self):
        super().__init__()

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass


class Mine(Munition):
    def __init__(self):
        super().__init__()

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass


class Missile(Munition):
    def __init__(self):
        super().__init__()

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass


class Agent(Munition):
    def __init__(self):
        super().__init__()

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass


class Drone(Munition):
    def __init__(self):
        super().__init__()

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass

