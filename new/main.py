
import pygame as pg
import sys
import random
from os import path
from settings import *
from sprites import *
from tilemap import *

# HUD functions


def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


def display_counter(surf, x, y, count, img):
    font = pg.font.Font('freesansbold.ttf', 32)
    text = font.render('{}'.format(count), True, WHITE)
    textRect = pg.Rect(x + 35, y, 35, 35)
    imgRect = pg.Rect(x, y, 35, 35)
    coinImg = pg.image.load(img)
    g.screen.blit(text, textRect)
    g.screen.blit(coinImg, imgRect)

#/////////////////////////////////////////////////////////////////////////////

# Game class: load_data, new, run, update, events, draw, draw_grid,


class Game:
    def __init__(self, mapIndex=0):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.game_folder = path.dirname(__file__)
        map_folder = path.join(self.game_folder, 'maps')
        self.mapList = []
        for i in MAPS:
            self.mapList.append(TiledMap(path.join(map_folder, i)))
        try:
            self.map = self.mapList[CURRENTMAP]
        except IndexError:
            self.map = self.mapList[0]
            self.load_data()
            self.intro_screen(self.endgame_img)
        self.load_data()
        
    def load_data(self):
        img_folder = path.join(self.game_folder, 'img')
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.intro_img = pg.image.load(path.join(img_folder, INTRO_IMG)).convert_alpha()
        self.death_img = pg.image.load(path.join(img_folder, DEATH_IMG)).convert_alpha()
        self.level_img = pg.image.load(path.join(img_folder, LEVEL_IMG)).convert_alpha()
        self.nextlevel_img = pg.image.load(path.join(img_folder, NEXTLEVEL_IMG)).convert_alpha()
        self.endgame_img = pg.image.load(path.join(img_folder, ENDGAME_IMG)).convert_alpha()
        self.player_img = pg.image.load(
            path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_images = {}
        # standard pistol bullets
        self.bullet_images['lg'] = pg.image.load(
            path.join(img_folder, BULLET_IMG)).convert_alpha()
        # red bullets for the machine gun use a different png
        self.bullet_images['rd'] = pg.image.load(
            path.join(img_folder, BULLET_IMG2)).convert_alpha()
        # small shot gun bullets are standard pistol bullets scaled down 10by10
        self.bullet_images['sm'] = pg.transform.scale(
            self.bullet_images['lg'], (10, 10))
        #regular zombie img
        self.mob_img = pg.image.load(
            path.join(img_folder, MOB_IMG)).convert_alpha()
        #big zombie img
        self.mob_img2 = pg.image.load(
            path.join(img_folder, MOB_IMG2)).convert_alpha()
        #boss img
        self.mob_img3 = pg.image.load(
            path.join(img_folder, MOB_IMG3)).convert_alpha()
        self.wall_img = pg.image.load(
            path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(
                path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        self.splat = pg.image.load(
            path.join(img_folder, SPLAT)).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (64, 64))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        
        #Loading of game objects from map file
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'zombie':
                Zombie(self, tile_object.x, tile_object.y)
            if tile_object.name == 'big_zombie':
                BigZombie(self, tile_object.x, tile_object.y)
            if tile_object.name == 'boss':
                Boss(self, tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name in ['health', 'shotgun','machinegun']:
                Item(self, obj_center, tile_object.name)
            if tile_object.name == 'coins':
                coins(self, tile_object.x, tile_object.y)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        

# Run class with music for the game level
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        
        #Loads music for specific level from GAME_SONGS list
        pg.mixer.music.load(GAME_SONGS[CURRENTMAP])
        pg.mixer.music.play(-1)
        
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        global CURRENTMAP
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        
        # mobs hit player and game ends on player death
        hits = pg.sprite.spritecollide(
            self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.intro_screen(self.death_img)
                CURRENTMAP = 0
                self.playing = False

        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

        # bullets hit mobs
        # hits is a dict each key of dict a mob that got hit, list of bullets that hits the mob
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        # for each mob that got hit subtract the health by bullets that hit
        for hit in hits:
            hit.health -= WEAPONS[self.player.weapon]['damage'] * \
                len(hits[hit])
            hit.vel = vec(0, 0)      
        # Enough Coins picked up to change level.
        if self.player.coin_count == NEXTLEVELCOINS:
            self.intro_screen(self.nextlevel_img, NEXTLEVELPOS, True)
            CURRENTMAP += 1
            self.playing = False

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            if isinstance(sprite, BigZombie):
                sprite.draw_health()
            if isinstance(sprite, Boss):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN,
                             self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN,
                             self.camera.apply_rect(wall.rect), 1)

        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
       
        # HUD functions
        draw_player_health(self.screen, 10, 10,
                           self.player.health / PLAYER_HEALTH)
        display_counter(self.screen, 130, 5, self.player.coin_count,
                        "img/coin_animation/Coin1.png")
        display_counter(self.screen, 200, 5,
                        self.player.killcount, "img/zombie_kill.png")
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
    
    
    # Function to diplay an information screen:
    #   - needs an image to display
    #   - can render text from the coin/coins to chenge level data 
    def intro_screen(self, img, pos = (0,0), responsive = False, wait = False):
        infoScreen = pg.display.set_mode((WIDTH, HEIGHT))
        # menu music
        pg.mixer.music.load('audio/menu_song.mp3')
        pg.mixer.music.play(-1)
        while True:
            infoScreen.blit(img, (0,0))
            # displays the coins require for next level on the change leevel screen
            if responsive:
                font = pg.font.SysFont("Courier New", 55)
                font.set_bold(True)
                text = font.render(str(NEXTLEVELCOINS),False, TEXTGREY)
                infoScreen.blit(text, pos)
            # displays the level number and has a pause rather than wait for player input
            if wait:
                font = pg.font.SysFont("Courier New", 75)
                font.set_bold(True)
                text = font.render(str(CURRENTMAP + 1),False, TEXTGREY)
                infoScreen.blit(text, pos)
                pg.display.flip()
                pg.time.wait(1000)
                return
            pg.display.flip()
            
            # The controls for the menu screen : ENTER to go, ESC to quit
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.quit()
                elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    #intro = False
                    return



# running the game
# start from the first map as CURRENTMAP                   
CURRENTMAP = 0
while True:
    # begin with the introduction menu
    Game().intro_screen(Game().intro_img)
    while True:
        # if the end of the maplist is reached, set the map back to zero and start the game loop again.
        if CURRENTMAP == (len(Game().mapList)):
            CURRENTMAP = 0
            break
        else:
            # generate a new game object, intialise the game, run the game
            Game().intro_screen(Game().level_img, LEVELPOS, False, True)
            g = Game()
            g.new()
            g.run()
