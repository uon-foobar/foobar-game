import pygame
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
wallRect = pygame.Rect(0, 0, tileSize, tileSize)
wallTile = spriteSheet.subsurface(wallRect)

# same as above
facingWallRect = pygame.Rect(0, 0, tileSize, tileSize)
facingWallTile = spriteSheet.subsurface(facingWallRect)

# no box currently - make them in main game loop as sprites
boxRect = pygame.Rect(tileSize*4, 0, tileSize, tileSize)
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
print(d.grid)
#place the sprite tiles according to the dungeon matrix
for x, y, tile in d:
    if tile == dungeonGenerator.EMPTY:
        screen.blit(wallTile, (x*tileSize, y*tileSize))
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
            screen.blit(wallTile, (x*tileSize, y*tileSize))

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

