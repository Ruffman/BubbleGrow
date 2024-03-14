from typing import Any
import pygame as pg

from projectile import Projectile
from game_internal import TYPE


# {name: [size, speed]}
SIZE_CLASS = {
    "scout": [50, 600],
    "fighter": [60, 500],
    "freighter": [70, 400],
    "tank": [80, 300],
    "capital": [120, 200],
}


class Tank(pg.sprite.Sprite):
    def __init__(self, o_type: str, size_class: str):
        pg.sprite.Sprite.__init__(self)
        self.surface = pg.display.get_surface()
        self.color = "white"
        self.object_type = o_type
        self.size_class = size_class
        self.size = SIZE_CLASS[self.size_class][0]
        self.speed = SIZE_CLASS[self.size_class][1]

        self.image = pg.transform.scale(pg.image.load(TYPE[o_type]['image']).convert(), (self.size, self.size))
        self.rect = self.image.get_rect()
        self.radius = self.size // 2

        self.projectile: Projectile


    def update(self, *args: Any, **kwargs: Any) -> None:
        pass

    def move(self, direction: pg.Vector2, dt):
        self.rect.center += direction * dt * self.speed

    def fire(self, target: pg.Vector2) -> Projectile:
        spawn_point = pg.Vector2(self.rect.center)
        direction = pg.Vector2(target - spawn_point).normalize()
        projectile = Projectile(spawn_point, direction, self.object_type)
        return projectile

    def get_position(self) -> pg.Vector2:
        return pg.Vector2(self.rect.center)


class Crosshair(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pg.image.load("art/tanks/crosshair.png")

        self.rect = self.image.get_rect()

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.center = pg.mouse.get_pos()


class AiTank(Tank):
    def __init__(self, o_type: str, size_class: str):
        super().__init__(o_type, size_class)

        self.fire_rate = 1.0
        self.fire_cd = self.fire_rate

        self.look_direction = pg.Vector2()
        self.speed = 100
        self.circle_distance = 300
        self.circle_buffer = 5

    def update(self, *args: Any, **kwargs: Any) -> None:
        dt = kwargs['dt']
        target: Tank = kwargs['target']
        self.fire_cd -= dt
        self.circle_target(dt, pg.Vector2(target.rect.center))

        pg.draw.line(pg.display.get_surface(), "red", self.rect.center, target.rect.center)

    def fire(self, target: pg.Vector2) -> Projectile:
        if self.fire_cd <= 0:
            self.fire_cd = self.fire_rate
            return super().fire(target)

    def look_at(self, target: pg.Vector2) -> None:
        target_direction = target - pg.Vector2(self.rect.center)
        if target_direction.length() > 0:
            target_direction = target_direction.normalize()
        self.look_direction = target_direction

    def move_in_direction(self, dt: float, direction: pg.Vector2) -> None:
        if direction.length() > 1:
            direction = direction.normalize()
        self.rect.center = self.rect.center + direction * self.speed * dt

    def circle_target(self, dt: float, target: pg.Vector2) -> None:
        distance_to_target = pg.Vector2(target - pg.Vector2(self.rect.center))
        self.look_at(target)
        if distance_to_target.length() > self.circle_distance + self.circle_buffer:
            self.move_in_direction(dt, self.look_direction)
        elif distance_to_target.length() < self.circle_distance:
            self.move_in_direction(dt, self.look_direction * -1)
        else:
            self.move_in_direction(dt, self.look_direction.rotate(90))
