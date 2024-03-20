from typing import Any
import pygame as pg
import math

from projectile import Projectile
from weapon import WeaponSystem, Turret
from game_internal import TYPE, ShipType, SHIP_TYPE_STATS, Faction



class Tank(pg.sprite.Sprite):
    def __init__(self, faction: Faction, ship_type: ShipType):
        pg.sprite.Sprite.__init__(self)
        self.surface = pg.display.get_surface()
        self.color = "white"
        self.faction = faction
        self.ship_type = ship_type
        self.size = SHIP_TYPE_STATS[self.ship_type][0]
        self.speed = SHIP_TYPE_STATS[self.ship_type][1]

        self.orig_image = pg.transform.scale(pg.image.load(TYPE[faction]['image']).convert(), (self.size, self.size))
        self.image = self.orig_image
        self.rect = self.image.get_rect()
        self.radius = self.size // 2

        self.mount_points: [pg.Vector2] = [pg.Vector2(-self.size // 3, -self.size // 3),
                                           pg.Vector2(self.size // 3, -self.size // 3)]
        self.weapons: [WeaponSystem] = []
        for pt in self.mount_points:
            self.weapons.append(Turret(pt))

        self.rotation_angle: float = 0
        self.orig_heading: pg.Vector2 = pg.Vector2(0, -1)
        self.heading: pg.Vector2 = pg.Vector2(0, 0)

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rotate_towards_mouse()

        self.draw_weapons()
        self.draw_heading()

    def move(self, direction: pg.Vector2, dt):
        self.rect.center += direction * dt * self.speed

    def fire(self, target: pg.Vector2) -> [Projectile]:
        new_projectiles = []
        for weapon in self.weapons:
            spawn_point = pg.Vector2(self.rect.center + weapon.current_position)
            direction = pg.Vector2(target - spawn_point).normalize()
            projectile = Projectile(spawn_point, direction, self.faction)
            if projectile:
                new_projectiles.append(projectile)
        return new_projectiles

    def get_position(self) -> pg.Vector2:
        return pg.Vector2(self.rect.center)

    def rotate_towards_mouse(self):
        direction: pg.Vector2 = pg.Vector2(pg.mouse.get_pos()) - pg.Vector2(self.rect.center)
        self.rotation_angle = self.orig_heading.angle_to(direction)

        old_center = self.rect.center
        self.image = pg.transform.rotate(self.orig_image, -self.rotation_angle)
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.heading = direction

        for weapon in self.weapons:
            weapon.rotate(self.rotation_angle)

    def draw_heading(self):
        length = 200
        start = self.rect.center
        end = start + self.heading.normalize() * length
        pg.draw.line(self.surface, "green", start, end)

    def draw_weapons(self):
        for weapon in self.weapons:
            weapon_pos = self.image.get_rect().center + weapon.current_position
            pg.draw.circle(self.image, "white", weapon_pos, 5)
            pg.draw.line(self.surface, "red", self.rect.center + weapon.current_position, pg.mouse.get_pos())


class Crosshair(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pg.image.load("art/tanks/crosshair.png")

        self.rect = self.image.get_rect()

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.center = pg.mouse.get_pos()


class AiTank(Tank):
    def __init__(self, faction: Faction, ship_type: ShipType):
        super().__init__(faction, ship_type)

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

        pg.draw.line(self.surface, "red", self.rect.center, target.rect.center)

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
