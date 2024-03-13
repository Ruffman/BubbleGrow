import pygame as pg
from tank import Tank



pg.init()
screen = pg.display.set_mode((1280, 720), pg.SCALED)
pg.display.set_caption("BubbleTanker")
pg.mouse.set_visible(False)
clock = pg.time.Clock()

background = pg.Surface(screen.get_size()).convert()
background.fill("blue")


player_tank = Tank()
player_tank.rect.center = (640, 360)

all_sprites = pg.sprite.Group((player_tank))

game_is_on = True
while game_is_on:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_is_on = False
        if event.type == pg.KEYDOWN:
            key = event.dict["key"]
            if key == pg.K_w:
                player_tank.move(0, -1)
            if key == pg.K_a:
                player_tank.move(-1, 0)
            if key == pg.K_s:
                player_tank.move(0, 1)
            if key == pg.K_d:
                player_tank.move(1, 0)

    all_sprites.update()


    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    pg.display.flip()

    clock.tick(60)

pg.quit()
