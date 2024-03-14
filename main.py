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


player_tank = Tank('player', 'tank')
player_tank.rect.center = (640, 360)
crosshair = Crosshair()
player_projectiles = pg.sprite.Group()

player_sprites = pg.sprite.Group([player_tank, crosshair])

ai_tank = AiTank('enemy', 'scout')
ai_tank.rect.center = (100, 100)
ai_tank_two = AiTank('enemy', 'freighter')
ai_tank_two.rect.center = (700, 700)

enemy_sprites = pg.sprite.Group([ai_tank, ai_tank_two])
enemy_projectiles = pg.sprite.Group()

game_is_on = True


def draw_all_sprites(display: pg.Surface):
    player_sprites.draw(display)
    enemy_sprites.draw(display)
    enemy_projectiles.draw(display)
    player_projectiles.draw(display)


def update_all_sprites(delta_time):
    player_sprites.update(dt=delta_time)
    enemy_sprites.update(dt=delta_time, target=player_tank)
    enemy_projectiles.update(dt=delta_time)
    player_projectiles.update(dt=delta_time)


while game_is_on:
    # process player inputs
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_is_on = False
        if event.type == pg.MOUSEBUTTONDOWN:
            button = event.dict['button']
            if button == 1:
                projectile = player_tank.fire(pg.Vector2(crosshair.rect.center))
                player_projectiles.add(projectile)
            if button == 3:
                new_enemy = AiTank('enemy', 'tank')
                new_enemy.rect.center = pg.mouse.get_pos()
                enemy_sprites.add(new_enemy)

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

    # enemy logic updates
    for enemy in enemy_sprites:
        # check collision with player projectiles
        for p in player_projectiles:
            if enemy.rect.colliderect(p.rect):
                enemy.kill()
                p.kill()
        # fire projectiles if able
        new_proj = enemy.fire(player_tank.get_position())
        if new_proj:
            enemy_projectiles.add(new_proj)

    # player logic updates
    for enemy in enemy_sprites:
        if pg.sprite.collide_circle(player_tank, enemy):
            enemy.kill()
            print("player hit an enemy actor")  # TODO player loses health
    for proj in enemy_projectiles:
        if pg.sprite.collide_circle(player_tank, proj):
            proj.kill()
            print("enemy projectile hit player")  # TODO player loses health

    update_all_sprites(dt)

    # render game here
    screen.blit(background, (0, 0))
    draw_all_sprites(screen)
    pg.display.flip()

    dt = clock.tick(60) / 1000

pg.quit()
