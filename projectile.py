from typing import Any

import pygame as pg

from game_internal import TYPE


class Projectile(pg.sprite.Sprite):
    def __init__(self, position: pg.Vector2, direction: pg.Vector2, p_type: str):
        super().__init__()

        self.image = pg.image.load(TYPE[p_type]['image']).convert()

        self.rect = self.image.get_rect()
        self.rect.center = position

        self.speed = 1000
        self.direction = direction

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.center = self.rect.center + self.direction * self.speed * kwargs["dt"]
