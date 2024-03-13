from typing import Any

import pygame as pg



class Projectile(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pg.image.load("art/tanks/bubble.png").convert()

        self.rect = self.image.get_rect()

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass
