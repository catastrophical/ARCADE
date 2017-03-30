import pygame as pg
import pytmx
from settings import *


class Camera:
    # this type of camera is drawing everything on the map in a different spot but the position of the things
    # will stay the same.
    
    # camera is having a widht and a height
    def __init__(self, width, height):
        mediator = None
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
