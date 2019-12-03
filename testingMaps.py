import pygame
import random
import os
import sys
import dungeonGenerator
from pygame.locals import *

pygame.init()
tileSize = 35
levelSize = 80  #!!!!!!!!!! MAX SIZE 35 on A32 PCs !!!!!!! Only square maps render well.

# folder paths and images for the map
main_dir = os.path.split(os.path.abspath(__file__))[0]
resource_path = os.path.join(main_dir, "resources")
image_path = os.path.join(resource_path, "images")

#initialise the screen and load the sprites 
screen = pygame.display.set_mode((levelSize * tileSize, levelSize * tileSize))
spriteSheet = pygame.image.load(os.path.join(image_path,"map_tilesheet.png")).convert()

#background - light grey
bgRect = pygame.Rect(tileSize*4, 0, tileSize, tileSize)
bgTile = spriteSheet.subsurface(bgRect)

#floor tile = grass
floorRect = pygame.Rect(tileSize*3, 0, tileSize, tileSize)
floorTile = spriteSheet.subsurface(floorRect)

#walltile = trees
wallRect1 = pygame.Rect(0, 0, tileSize, tileSize)
wallTile1 = spriteSheet.subsurface(wallRect1)
wallRect2 = pygame.Rect(tileSize*4, 0, tileSize, tileSize)
wallTile2 = spriteSheet.subsurface(wallRect2)
wallRect3 = pygame.Rect(tileSize*5, 0, tileSize, tileSize)
wallTile3 = spriteSheet.subsurface(wallRect3)
wallRect4 = pygame.Rect(tileSize*6, 0, tileSize, tileSize)
wallTile4 = spriteSheet.subsurface(wallRect4)
wallRect5 = pygame.Rect(tileSize*7, 0, tileSize, tileSize)
wallTile5 = spriteSheet.subsurface(wallRect5)
wallRect6 = pygame.Rect(tileSize*8, 0, tileSize, tileSize)
wallTile6 = spriteSheet.subsurface(wallRect6)

# same as above
facingWallRect = pygame.Rect(0, 0, tileSize, tileSize)
facingWallTile = spriteSheet.subsurface(facingWallRect)

# no box currently - make them in main game loop as sprites
boxRect = pygame.Rect(tileSize*9, 0, tileSize, tileSize)
boxTile = spriteSheet.subsurface(boxRect)  

#doors are just grass openings 
doorRect = pygame.Rect(tileSize*3, 0, tileSize, tileSize)
doorTile = spriteSheet.subsurface(doorRect)

 # doors are just grass openings
doorSideRect = pygame.Rect(tileSize*3, 0, tileSize, tileSize)
doorSideTile = spriteSheet.subsurface(doorSideRect)

# init the dungeon module
d = dungeonGenerator.dungeonGenerator(levelSize, levelSize)
d.placeRandomRooms(3, 9, 2, 4, 1000)
d.generateCorridors()
d.connectAllRooms(30)
d.pruneDeadends(20)
d.placeWalls()

# the game intro
def gameIntro():
    def blit_text(surface, text, pos, font, color=pygame.Color('black')):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.

    introString = "                      Welcome to The Eternal Forest. \n\n Your job is to move through the forest maze killing monsters and finding doors. \n\n The more sections of the forest you pass through the higher your points will \n be and the harder the enemies get. \n\n Move with W/A/S/D and shoot with UP/DOWN/LEFT/RIGHT. \n\n                       <--Press ENTER to begin. --> "

    introScreen = pygame.display.set_mode((1024, 800))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == KEYDOWN and event.key == K_RETURN:
                #intro = False
                return
        font = pygame.font.SysFont("Courier New", 20)
        introScreen.fill([50,50,50])
        blit_text(introScreen, introString, (50, 50), font, [230,230,230])
        pygame.display.flip()
'''
gameIntro()
#place the sprite tiles according to the dungeon matrix
for x, y, tile in d:
    if tile == dungeonGenerator.EMPTY:
        trees = [wallTile1,wallTile2,wallTile3,wallTile4,wallTile5,wallTile6]
        screen.blit(random.choice(trees), (x*tileSize, y*tileSize))
    if tile == dungeonGenerator.FLOOR:
        screen.blit(floorTile, (x*tileSize, y*tileSize))
    elif tile == dungeonGenerator.CORRIDOR:
        screen.blit(floorTile, (x*tileSize, y*tileSize))
    elif tile == dungeonGenerator.DOOR:
        # rotate the door tile accordingly
        # no need to check bounds since a door tile will never be against the edge
        #if d.grid[x+1][y] == dungeonGenerator.WALL:
        screen.blit(doorTile, (x*tileSize, y*tileSize))
        #else:
         #   screen.blit(doorSideTile, (x*tileSize, y*tileSize))
    elif tile == dungeonGenerator.WALL:
        # if the wall tile is facing us lets render a different one
        #if y == levelSize-1 or d.grid[x][y+1] != dungeonGenerator.WALL:
         #   screen.blit(facingWallTile, (x*tileSize, y*tileSize))
        #else:
            trees = [wallTile1,wallTile2,wallTile3,wallTile4,wallTile5,wallTile6]
            screen.blit(random.choice(trees), (x*tileSize, y*tileSize))

# prune dead ends
for de in d.deadends:
    screen.blit(boxTile, (de[0] * tileSize, de[1] * tileSize))

# quit function for testing.
while True:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    pygame.display.flip()

'''