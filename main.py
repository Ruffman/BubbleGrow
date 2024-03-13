import pygame as pg
from tank import Tank, Crosshair
from projectile import Projectile



pg.init()
screen = pg.display.set_mode((1000, 800), pg.SCALED)
pg.display.set_caption("BubbleTanker")
pg.mouse.set_visible(False)
clock = pg.time.Clock()
dt = 0

background = pg.Surface(screen.get_size()).convert()
background.fill("blue")


player_tank = Tank()
player_tank.rect.center = (640, 360)

ai_tank = Tank()
ai_tank.rect.center = (100, 100)

crosshair = Crosshair()

all_sprites = pg.sprite.Group([player_tank, ai_tank, crosshair])

game_is_on = True
while game_is_on:
    # process player inputs
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_is_on = False
        if event.type == pg.MOUSEBUTTONDOWN:
            button = event.dict['button']
            if button == 1:
                projectile = player_tank.fire(pg.Vector2(crosshair.rect.center))
                all_sprites.add(projectile)
            if button == 3:
                spawn_point = pg.Vector2(ai_tank.rect.center)
                direction = pg.Vector2(pg.Vector2(crosshair.rect.center) - spawn_point).normalize()
                projectile = Projectile(spawn_point, direction)
                all_sprites.add(projectile)

    keys_pressed = pg.key.get_pressed()

    # player movement
    if keys_pressed[pg.K_w]:
        player_tank.move(0, -1, dt)
    if keys_pressed[pg.K_a]:
        player_tank.move(-1, 0, dt)
    if keys_pressed[pg.K_s]:
        player_tank.move(0, 1, dt)
    if keys_pressed[pg.K_d]:
        player_tank.move(1, 0, dt)

    # Game logic updates
    all_sprites.update(dt=dt)


    # render game here
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    pg.display.flip()

    dt = clock.tick(60) / 1000

pg.quit()
