import pygame as pg
from tank import Tank, AiTank, Crosshair



pg.init()
screen = pg.display.set_mode((1000, 800), pg.SCALED)
pg.display.set_caption("BubbleTanker")
pg.mouse.set_visible(False)
clock = pg.time.Clock()
dt = 0

background = pg.Surface(screen.get_size()).convert()
background.fill("blue")


player_tank = Tank('player')
player_tank.rect.center = (640, 360)
crosshair = Crosshair()

all_sprites = pg.sprite.Group([player_tank, crosshair])

ai_tank = AiTank()
ai_tank.rect.center = (100, 100)
all_sprites.add(ai_tank)
ai_tank_two = AiTank()
ai_tank_two.rect.center = (700, 700)
all_sprites.add(ai_tank_two)
enemy_sprites = pg.sprite.Group([ai_tank, ai_tank_two])


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
                new_enemy = AiTank()
                new_enemy.rect.center = pg.mouse.get_pos()
                enemy_sprites.add(new_enemy)
                all_sprites.add(new_enemy)

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
    for enemy in enemy_sprites:
        new_proj = enemy.fire(player_tank.get_position())
        if new_proj:
            all_sprites.add(new_proj)



    all_sprites.update(dt=dt)


    # render game here
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    pg.display.flip()

    dt = clock.tick(60) / 1000

pg.quit()
