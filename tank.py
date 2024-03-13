from typing import Any

import pygame as pg
from projectile import Projectile


# {name: [size, speed]}
SIZE_CLASS = {
    "scout": [50, 600],
    "fighter": [60, 500],
    "freighter": [70, 400],
    "tank": [80, 300],
    "capital": [120, 200],
}


class Tank(pg.sprite.Sprite):
    def __init__(self, o_type: str):
        pg.sprite.Sprite.__init__(self)
        self.surface = pg.display.get_surface()
        self.color = "white"
        self.object_type = o_type
        self.size_class = "tank"
        self.size = SIZE_CLASS[self.size_class][0]
        self.speed = SIZE_CLASS[self.size_class][1]

        self.image = pg.image.load("art/tanks/bubble.png")
        self.rect = self.image.get_rect()

        self.projectile: Projectile


    def update(self, *args: Any, **kwargs: Any) -> None:
        pass

    def move(self, x_axis, y_axis, dt):
        self.rect.center += pg.Vector2(x_axis*self.speed*dt, y_axis*self.speed*dt)

    def fire(self, target: pg.Vector2) -> Projectile:
        spawn_point = pg.Vector2(self.rect.center)
        direction = pg.Vector2(target - spawn_point).normalize()
        projectile = Projectile(spawn_point, direction, self.object_type)
        return projectile


class Crosshair(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pg.image.load("art/tanks/crosshair.png")

        self.rect = self.image.get_rect()

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.center = pg.mouse.get_pos()
