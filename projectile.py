from typing import Any

import pygame as pg



class Projectile(pg.sprite.Sprite):
    def __init__(self, position: pg.Vector2, direction: pg.Vector2):
        super().__init__()

        self.image = pg.image.load("art/tanks/bubble.png").convert()

        self.rect = self.image.get_rect()
        self.rect.center = position

        self.speed = 1000
        self.direction = direction

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.center = self.rect.center + self.direction * self.speed * kwargs["dt"]
