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

# Audio
GAME_SONGS = ['audio/level1.mp3', 'audio/level2.mp3', 
              'audio/level1.mp3', 'audio/level2.mp3',
              'audio/level1.mp3', 'audio/level2.mp3', 
              'audio/level1.mp3', 'audio/level2.mp3']

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Foobar"
BGCOLOR = BROWN

MAPS = ['level1.tmx', 'level2.tmx', 'level3.tmx', 'level4.tmx',
        'level5.tmx', 'level6.tmx', 'level7.tmx', 'level8.tmx']

NEXTLEVELCOINS = 2


TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'tileGreen_39.png'

# Load screen messages
INTRO = "                         Welcome to The foobar. \n\n\n Your job is to move through the world killing zombies and finding powerups. \n\n Collect coins to move to the next level, each level will get slightly more \n difficult! \n\n Move with W/A/S/D or UP/DOWN/LEFT/RIGHT and shoot with SPACE . \n\n\n                     <-- Press ENTER to begin. --> "
NEWLEVEL = "                      Wow! You collected {} coins!!!! \n\n\n                   You get to continue to the next level!\n\n                      <-- Press ENTER to continue. -->".format(
    NEXTLEVELCOINS)
DEAD = "                      !!!!!! OH NO YOU DIED !!!!!! \n\n\n\n                       If you want to START AGAIN: \n\n                      <-- Press ENTER to begin. --> \n\n\n                          If you want to QUIT: \n\n                           <-- Press ESC -->"
ENDGAME = "                     Congratulations! You beat the game!!!! \n\n                 You must be a really fantastic Zombie Killer!\n\n\n\n                  If you'd like to play again , just press: \n\n                              <-- ENTER --> \n\n\n\n                           Otherwise quit with:\n\n                               <-- ESC -->"
INTRO_IMG = 'intro.png'

INFOPOS = (50, 50)
NEWLEVELPOS = (0, 300)
LEVELPOS = (450, 350)

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
                'machinegun': 'machinegun.png',}
HEALTH_PACK_AMOUNT = 20

# Coins
COIN_IMAGE_LIST = [(pg.image.load("img/coin_animation/Coin1.png")),
                   (pg.image.load("img/coin_animation/Coin2.png")),
                   (pg.image.load("img/coin_animation/Coin3.png")),
                   (pg.image.load("img/coin_animation/Coin4.png")),
                   (pg.image.load("img/coin_animation/Coin5.png")),
                   (pg.image.load("img/coin_animation/Coin6.png"))]
