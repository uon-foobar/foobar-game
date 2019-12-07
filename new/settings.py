import pygame as pg
vec = pg.math.Vector2

# Basic Tile info
TITLE = "Foobar"
TILESIZE = 64
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
FPS = 60
WALL_IMG = 'tileGreen_39.png'
NEXTLEVELCOINS = 5 # This is the number of coins you need to collect to move to the next level.

# define some colors (R, G, B)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
TEXTGREY = [204,204,204]

# Audio
#Level Songs = list index+1 defines the song played in a loop on that level
GAME_SONGS = ['audio/level1.mp3', 'audio/level2.mp3',
              'audio/level1.mp3', 'audio/level2.mp3',
              'audio/level1.mp3', 'audio/level2.mp3',
              'audio/level1.mp3', 'audio/level2.mp3',
              'audio/level1.mp3']

#MENU_SONG - Defines the song played on the menu screen
MENU_SONG = 'audio/menu_song.mp3'


#Sounds for collisions, gunfire etc.
COIN_COLLECT = 'audio/coin_collect.wav'
ZOMBIE_DEATH = 'audio/zombie_death.wav'
HEALTH_POWERUP = 'audio/health_powerup.ogg'
PISTOL_FIRED = 'audio/pistol.ogg'
SHOTGUN_FIRED = 'audio/shotgun.ogg'
MACHINEGUN_FIRED = 'audio/machine_gun.wav'
MOB_PUNCH_SOUND = 'audio/punch.wav'
GUN_PICKUP = 'audio/gun_pickup.wav'

# Sound Channels - Different sounds must be on different channels if they are
#to be played concurrently
ITEM_COLLECT_CHANNEL = 4
MOB_PUNCH_CHANNEL = 3
WEAPON_FIRE_CHANNEL = 7

# Map list, can re-order them
MAPS = ['level4.tmx', 'level1.tmx', 'level2.tmx', 'level3.tmx', 'level9.tmx',
        'level5.tmx', 'level6.tmx', 'level7.tmx', 'level8.tmx']

# Load screen messages
INTRO_IMG = 'intro.png'
DEATH_IMG = 'dead.png'
LEVEL_IMG = 'level.png'
NEXTLEVEL_IMG = 'nextlevel.png'
ENDGAME_IMG = 'endgame.png'
# the two positions for the responsive printing to the screen for the menus.
NEXTLEVELPOS = (680,205)
LEVELPOS = (585,295)

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 280
PLAYER_ROT_SPEED = 200 # rotation speed of the player as he moves
PLAYER_IMG = 'manBlue_gun.png' 
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35) # hitbox
BARREL_OFFSET = vec(30, 10) # position of the gun barrel on the player image

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
BULLET_LIFETIME = 1000 # bullet lasts for 1 second
BULLET_RATE = 150 # how fast it shoots
KICKBACK = 100 # how far the player is pushed back
GUN_SPREAD = 5 # how much angle the bullet spreads from the barrel
BULLET_DAMAGE = 10

# Mob settings
MOB_IMG = 'zombie1_hold.png'
MOB_SPEED = 150
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
SPLAT = 'splat red.png'
ATTACK_RADIUS = 450

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

# Coins list - Contains a list of snapshots of a coin rotating
#Iterated through by the coin class to showw a coin rotating
COIN_IMAGE_LIST = [(pg.image.load("img/coin_animation/Coin1.png")),
                   (pg.image.load("img/coin_animation/Coin2.png")),
                   (pg.image.load("img/coin_animation/Coin3.png")),
                   (pg.image.load("img/coin_animation/Coin4.png")),
                   (pg.image.load("img/coin_animation/Coin5.png")),
                   (pg.image.load("img/coin_animation/Coin6.png"))]
