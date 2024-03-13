import pygame as pg
from tank import Tank, Crosshair



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

crosshair = Crosshair()

all_sprites = pg.sprite.Group([player_tank, crosshair])

game_is_on = True
while game_is_on:
    # process player inputs
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_is_on = False

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
