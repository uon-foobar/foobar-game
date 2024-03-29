import pygame as pg
import pytmx
from settings import *

'''
The TiledMap function is a template provided by the pytmx library.
We have used this to load the map.tmx files we created in the Tiled software.
This was in order to produce more maps more quickly, in essence we understand the approach used:
    That is to create a matirx to represent the map and load the sprites at those coordinates
    depending on the value there.
The details of the library and function were not written by us.
Link to docs: www.pypi.org/project/PyTMX/
'''

# a helper function to simplify the collision between two sprites.
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

# This function loads the screen according to the maps produced in the Tiled software.
class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


# This function controls the size of the camera in relation to the map size. it follows the player position(x,y)  
class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
    
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)
    
    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
