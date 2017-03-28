import pygame as pg
import pytmx
from settings import *

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class Map:
    # initialize the map and load the filename
    def __init__(self, filename):
        # list where we put all the maps tiles
        self.data = []
        # send it to filename that opens the file, and reads it all in and put it all in self.data
        with open(filename, 'rt') as f:
            for line in f:
                # strip function removes invisible /newline so the camera dosent go one tile to far
                self.data.append(line.strip())
        # how many tiles widht the map is. the length of one of the lines. here line 0
        self.tilewidth = len(self.data[0])
        # tileheight is the length of the list
        self.tileheight = len(self.data)
        # pixel width and height of the screen tilewidth * tilesize
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

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

class Camera:
    # this type of camera is drawing everything on the map in a different spot but the position of the things
    # will stay the same.

    # camera is having a widht and a height
    def __init__(self, width, height):
        # we use a rectangle to track it. 0, 0 is how far we need to put the offset
        self.camera = pg.Rect(0, 0, width, height)
        # widht and height are named so theyre easier to refer to
        self.width = width
        self.height = height

        # move the entity on the screen (wall, enemy ect.)
    def apply(self, entity):
        # move.rect makes a new rectangle that is moved by the value of the parameters self.camera.topleft
        return entity.rect.move(self.camera.topleft)
        #move the cameras rect
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)
        #update offset
        #where the x and y of the camera is gonna shift to
        # / 2 sets the player in the middle of the camera
        # -target moves the camera the oposite way of the player
    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        # adjust the x and y position of the camera
        self.camera = pg.Rect(x, y, self.width, self.height)
