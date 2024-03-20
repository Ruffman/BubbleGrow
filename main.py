import pygame as pg
from tank import Tank, AiTank, Crosshair

from game_internal import ShipType, Faction



DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 1024

pg.init()
screen = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pg.SCALED)
pg.display.set_caption("BubbleTanker")
pg.mouse.set_visible(False)
clock = pg.time.Clock()
dt = 0

background = pg.image.load("art/background/cool_red_space.jpg").convert()


player_tank = Tank(Faction.PLAYER, ShipType.TANK)
player_tank.rect.center = (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2)
crosshair = Crosshair()
player_projectiles = pg.sprite.Group()

player_sprites = pg.sprite.Group([player_tank, crosshair])

ai_tank = AiTank(Faction.ENEMY, ShipType.SCOUT)
ai_tank.rect.center = (100, 100)
ai_tank_two = AiTank(Faction.ENEMY, ShipType.TANK)
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
                new_enemy = AiTank(Faction.ENEMY, ShipType.TANK)
                new_enemy.rect.center = pg.mouse.get_pos()
                enemy_sprites.add(new_enemy)

    keys_pressed = pg.key.get_pressed()

    # player movement#
    player_direction = pg.Vector2(0, 0)
    if keys_pressed[pg.K_w]:
        player_direction += pg.Vector2(0, -1)
    if keys_pressed[pg.K_a]:
        player_direction += pg.Vector2(-1, 0)
    if keys_pressed[pg.K_s]:
        player_direction += pg.Vector2(0, 1)
    if keys_pressed[pg.K_d]:
        player_direction += pg.Vector2(1, 0)
    if player_direction.length() > 0:
        player_direction = player_direction.normalize()
    player_tank.move(player_direction, dt)

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

    # this should come after update, but for debug purposes it's before for now
    screen.blit(background, (0, 0))

    update_all_sprites(dt)

    # render game here
    draw_all_sprites(screen)
    pg.display.flip()

    dt: float = clock.tick(60) / 1000

pg.quit()
