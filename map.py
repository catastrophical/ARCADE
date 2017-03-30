import pygame as pg
import pytmx
from settings import *

'''class Map:
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
        self.height = self.tileheight * TILESIZE'''
