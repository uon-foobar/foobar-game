import pygame as pg
from random import uniform
from settings import *
from tilemap import collide_hit_rect
vec = pg.math.Vector2


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.coin_count = 0
        self.killcount = 0
        self.weapon = 'pistol'

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
        if keys[pg.K_SPACE]:

            self.shoot()

    def shoot(self):
        if self.weapon == 'pistol':
                pg.mixer.Sound.play(pg.mixer.Sound('audio/pistol.ogg'))
        if self.weapon == 'shotgun':
                pg.mixer.Sound.play(pg.mixer.Sound('audio/shotgun.ogg'))
        if self.weapon == 'machinegun':
                pg.mixer.Sound.play(pg.mixer.Sound('audio/pistol.ogg')) ### Richard

        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            self.vel = vec(-WEAPONS[self.weapon]
                           ['kickback'], 0).rotate(-self.rot)
            for i in range(WEAPONS[self.weapon]['bullet_count']):
                spread = uniform(-WEAPONS[self.weapon]
                                 ['spread'], WEAPONS[self.weapon]['spread'])
                Bullet(self.game, pos, dir.rotate(spread))
                
    def collect_coins(self):
        pg.mixer.Channel(2).play(pg.mixer.Sound('audio/coin_collect.wav'))
        self.coin_count += 1

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def add_health(self, amount):
        pg.mixer.Channel(5).play(pg.mixer.Sound('audio/health_powerup.ogg'))
        #pg.mixer.Sound.play(pg.mixer.Sound('audio/health_powerup.ogg'))
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if self.TYPE == 1:
            self.image = game.mob_img
        if self.TYPE == 2:
            self.image = game.mob_img2
        if self.TYPE == 3:
            self.image = game.mob_img3
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.rect.center = (x, y)
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = self.HEALTH

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        if self.TYPE == 1:
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        if self.TYPE == 2:
            self.image = pg.transform.rotate(self.game.mob_img2, self.rot)
        if self.TYPE == 3:
            self.image = pg.transform.rotate(self.game.mob_img3, self.rot)
        # self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(self.SPEED, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.game.player.killcount += 1
            pg.mixer.Sound.play(pg.mixer.Sound('audio/zombie_death.wav'))
            self.kill()
            
    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / self.HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < self.HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)


class Zombie(Mob):
    TYPE = 1
    HEALTH = MOB_HEALTH
    SPEED = MOB_SPEED


class BigZombie(Mob):
    TYPE = 2
    HEALTH = MOB_HEALTH2
    SPEED = MOB_SPEED2


class Boss(Mob):
    TYPE = 3
    HEALTH = MOB_HEALTH3
    SPEED = MOB_SPEED3


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_images[WEAPONS[game.player.weapon]
                                        ['bullet_size']]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        #spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir * WEAPONS[game.player.weapon]['bullet_speed']
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['bullet_lifetime']:
            self.kill()


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

# Item Sprites - using for health, and maybe guns


class Item(pg.sprite.Sprite):
    # type - healthpack , guns etc
    def __init__(self, game, pos, type):
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.rect.center = pos
        self.pos = pos


class coins(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.index = 0
        self.image = COIN_IMAGE_LIST[self.index]
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.center = self.pos

    def update(self):
        self.index += 1
        if self.index >= len(COIN_IMAGE_LIST):
            self.index = 0
        self.image = COIN_IMAGE_LIST[self.index]
