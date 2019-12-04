import pygame as pg
import pytmx
from settings import *


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE


class TiledMap:
    def __init__(self, filename):
        # pytmx reads our tiled map files
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        # width = 50 and tilewidth is 64 so total map is 50*64
        self.width = tm.width * tm.tilewidth
        # Same for height
        self.height = tm.height * tm.tileheight
        # tmxdata holds all the stuff so we can refer to it
        self.tmxdata = tm

    def render(self, surface):
        # Takes a pygame surface and draws all the tiles of map onto it
        ti = self.tmxdata.get_tile_image_by_gid
        # gid is the unique id for each tile - global id, so aliasing the command as ti
        for layer in self.tmxdata.visible_layers:
            # going through all visible layers in our map
            if isinstance(layer, pytmx.TiledTileLayer):
                # now getting each x y and gid in the tiled tile layer
                # draw it at location() and looping for each in order of the layers, so ground layer is drawn first and so on
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        # draw surface however big the tilemap is
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
# Two options to move the camera now sprite or rect

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        # func that takes in a rect instead of a sprite
        # return the rect moved by whatever the camera offset is
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
