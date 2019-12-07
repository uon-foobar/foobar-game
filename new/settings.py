import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)
TEXTGREY = [204,204,204]

# Audio
GAME_SONGS = ['audio/level1.mp3', 'audio/level2.mp3',
              'audio/level1.mp3', 'audio/level2.mp3',
              'audio/level1.mp3', 'audio/level2.mp3',
              'audio/level1.mp3', 'audio/level2.mp3']

COIN_COLLECT = 'audio/coin_collect.wav'

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Foobar"
BGCOLOR = BROWN

MAPS = ['level1.tmx', 'level2.tmx', 'level3.tmx', 'level4.tmx',
        'level5.tmx', 'level6.tmx', 'level7.tmx', 'level8.tmx']
NEXTLEVELCOINS = 1



TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'tileGreen_39.png'

# Load screen messages
INTRO_IMG = 'intro.png'
DEATH_IMG = 'dead.png'
LEVEL_IMG = 'level.png'
NEXTLEVEL_IMG = 'nextlevel.png'
ENDGAME_IMG = 'endgame.png'

#INFOPOS = (50, 50)
NEXTLEVELPOS = (680,205)
LEVELPOS = (585,295)

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 280
PLAYER_ROT_SPEED = 200
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)

# Gun settings
BULLET_IMG = 'bullet.png'
BULLET_IMG2 = 'bullet2.png'
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 500,
                     'bullet_lifetime': 1000,
                     'rate': 250,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 10,
                     'bullet_size': 'lg',
                     'bullet_count': 1}
WEAPONS['shotgun'] = {'bullet_speed': 500,
                      'bullet_lifetime': 500,
                      'rate': 500,
                      'kickback': 300,
                      'spread': 20,
                      'damage': 5,
                      'bullet_size': 'sm',
                      'bullet_count': 12}
WEAPONS['machinegun'] = {'bullet_speed': 500,
                         'bullet_lifetime': 1500,
                         'rate': 150,
                         'kickback': 300,
                         'spread': 5,
                         'damage': 10,
                         'bullet_size': 'rd',
                         'bullet_count': 1}
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150
KICKBACK = 100
GUN_SPREAD = 5
BULLET_DAMAGE = 10

# Mob settings
MOB_IMG = 'zombie1_hold.png'
MOB_SPEED = 150
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
SPLAT = 'splat red.png'
ATTACK_RADIUS = 300
# Zombie
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20

# BigZombie
MOB_IMG2 = 'zombie1_hold2.png'
MOB_SPEED2 = 100
MOB_HEALTH2 = 200

# Boss
MOB_IMG3 = 'boss.png'
MOB_SPEED3 = 300
MOB_HEALTH3 = 300

# Items
ITEM_IMAGES = {'health': 'health_pack.png',
               'shotgun': 'shotgun.png',
               'machinegun': 'machinegun.png', }
HEALTH_PACK_AMOUNT = 20

# Coins
COIN_IMAGE_LIST = [(pg.image.load("img/coin_animation/Coin1.png")),
                   (pg.image.load("img/coin_animation/Coin2.png")),
                   (pg.image.load("img/coin_animation/Coin3.png")),
                   (pg.image.load("img/coin_animation/Coin4.png")),
                   (pg.image.load("img/coin_animation/Coin5.png")),
                   (pg.image.load("img/coin_animation/Coin6.png"))]
