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

#Main player class, has attributes such as player image,player health,player hitbox,player position and velocity,starting coins,kills and weapon.
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

#Function that changes the player movement and the shooting according to the key presses.
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
        #Generates a sound for a particular gun when shooting
        if self.weapon == 'pistol':
            pg.mixer.Channel(WEAPON_FIRE_CHANNEL).play(pg.mixer.Sound(PISTOL_FIRED))
        if self.weapon == 'shotgun':
            pg.mixer.Channel(WEAPON_FIRE_CHANNEL).play(pg.mixer.Sound(SHOTGUN_FIRED ))
        if self.weapon == 'machinegun':
            pg.mixer.Channel(WEAPON_FIRE_CHANNEL).play(pg.mixer.Sound(MACHINEGUN_FIRED))
            
             


            
        
        
        now = pg.time.get_ticks()
        #Defines the rate of fire of the weapon held by the player
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
        #Changing the position of bullets so they dont fire from the centre of the player, instead from the gun
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
        #How much the player moves back upon shooting the gun
            self.vel = vec(-WEAPONS[self.weapon]
                           ['kickback'], 0).rotate(-self.rot)
        #How the bullet behaves, does it spread in all directions or shoots in one line
            for i in range(WEAPONS[self.weapon]['bullet_count']):
                spread = uniform(-WEAPONS[self.weapon]
                                 ['spread'], WEAPONS[self.weapon]['spread'])
                Bullet(self.game, pos, dir.rotate(spread))

    #Function that rotates the static image on the player acording to the player movement,checks for collisions with walls and mobs
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
        if pg.sprite.spritecollide(self, self.game.mobs, False, collided=None):
            pg.mixer.Channel(MOB_PUNCH_CHANNEL).play(pg.mixer.Sound(MOB_PUNCH_SOUND))
        self.item_pickup()
        
    #Function that adds health to player, used by the health kit item, if player health is full player doesnt pick it up
    def add_health(self, amount):
        pg.mixer.Channel(5).play(pg.mixer.Sound(HEALTH_POWERUP))
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH
    #Function for picking up the item if the item loc and player loc is same it is picked up by the player and kills the sprite        
    def item_pickup(self):
        hits = pg.sprite.spritecollide(self, self.game.items, False)
        for hit in hits:
            if hit.type == 'health' and self.health < PLAYER_HEALTH:
                hit.kill()
                self.add_health(HEALTH_PACK_AMOUNT)
            if hit.type == 'shotgun':
                pg.mixer.Channel(ITEM_COLLECT_CHANNEL).play(
                    pg.mixer.Sound(COIN_COLLECT))
                hit.kill()
                self.weapon = 'shotgun'
            if hit.type == 'machinegun':
                pg.mixer.Channel(ITEM_COLLECT_CHANNEL).play(
                    pg.mixer.Sound(COIN_COLLECT))
                hit.kill()
                self.weapon = 'machinegun'
        
        if pg.sprite.spritecollide(self, self.game.coins, True, collided=None):
            pg.mixer.Channel(2).play(pg.mixer.Sound(COIN_COLLECT))
            self.coin_count += 1
        

#Main mob class, contains attributes for type of mob,hitbox,position,velocity,health
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
        #Uses this to check the location of player on the map
        self.target = game.player
        self.health = self.HEALTH

    def update(self):
        #Determines the distance of the mob from the player
        target_distance = self.target.pos - self.pos
        #Checks if the player is in its 'Attack Radius', if yes then the mob charges towards the player using player's location
        if target_distance.length_squared() < ATTACK_RADIUS**2:
            self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
            #Gets the images according to mob type
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
        #How mob dies and the sprite is deleted and killcount increases
        if self.health <= 0:
            self.game.player.killcount += 1
            pg.mixer.Sound.play(pg.mixer.Sound(ZOMBIE_DEATH))
            self.kill()
            #Blood spatter effect on mob death
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))
    #Draws the health of the zombie on the screen above the zombie, changes health bar colour according to health        
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

#Class for the bullet sprites,img location,pos,velocity,and the spawn time
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
#Bullet sprite dies if it collides with the wall or bullet lifetime is over
    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['bullet_lifetime']:
            self.kill()
#Class for the walls,and other obstacles, defines where the obstacles are
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



# Item Sprites - Used for guns and health,their position,img,type etc
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
