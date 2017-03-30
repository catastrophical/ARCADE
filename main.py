#Imports
#Import pygame som pg, pygame er vores framework og i resten af programmet kaldes det pg
import pygame as pg
#Importere sys som er en oversaetter
import sys
#Importere random som giver mulighed for at lave random stuff
from random import choice, random
#importere operativsystemets path eks. C:\something\something\ mac: /Users/
from os import path
#importere programkode fra settings, sprites og tilemap
from settings import *
from mediator import *
from player import *
from obstacle import *
from tiledmap import *
from map import *

from camera import *




#Vi laver en klasse der hedder Game
class Game:
    #Klassen får en metode til at initialisere sig selv
    def __init__(self):
        #Initialisering af lyd
        mediator = None
        pg.mixer.pre_init(44100, -16, 4, 2048)
        #Initialisering af pygame
        pg.init()
       
        #sets FULLSCREEN and makes a window for the game, and gets the WIDTH and HEIGHT from setting
        self.screen = pg.display.set_mode((WIDTH, HEIGHT),pg.FULLSCREEN)
        #sets the title of screen to TITLE from settings
        pg.display.set_caption(TITLE)
        #clock initialiseres til at tælle millisekunderne fra spillet startes
        self.clock = pg.time.Clock()
        #Kører metoden til at hente data fra spillets game_folder, img_folder, snd_folder og music_folder
        self.load_data()
        #Definere metoden load_data
    def load_data(self):
        #game_folder tildeles værdien af path fra main.py dirname
        game_folder = path.dirname(__file__)
        #img_folder tildeles værdien af en path inde i game_folder som har string-værdien 'img
        img_folder = path.join(game_folder, 'img')
        #snd_folder tildeles værdien af en path inde i game_folder som har string-værdien 'snd
        snd_folder = path.join(game_folder, 'snd')
        #img_folder tildeles værdien af en path inde i game_folder som har string-værdien 'music
        music_folder = path.join(game_folder, 'music')
        #Vi forstår ikke hvorfor den her er anderledes???
        self.map_folder = path.join(game_folder, 'maps')
        #Vi skal lige fatte .convertalpha
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        #Initialisere en effect_sound liste
        self.effects_sounds = {}
        #Et for-each loop der Tildeler værdier til listen effect_sound som hentes i EFFECTS_SOUNDS i settings
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))

    def new(self):
        # initialize all variables and do all the setup for a new game
        # all_sprites bliver opdateret i forhold til sine lag
        
        
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        
        self.mediator = Mediator()
        
        #self.mediator.pplayer = Player()

        self.map = TiledMap(path.join(self.map_folder, 'first_level.tmx'))
        self.mediator.map = self.map
        self.map.mediator = self.mediator
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
                #Når mediatorens player bliver til den player vi lige har oprettet
                #og derfor kan de snakke sammen
                self.mediator.player = self.player
                self.player.mediator = self.mediator

                   

            if tile_object.name == 'wall':
                self.obstacle = Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
                self.mediator.obstacle = self.obstacle
                self.obstacle.mediator = self.mediator
                         




        #spawn the camera and set the widht and height of the map so we know the area the camera can move in
        self.camera = Camera(self.map.width, self.map.height)
        self.mediator.camera = self.camera
        self.camera.mediator = self.mediator
        self.draw_debug = False
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            self.update()
            self.draw()

    def died(self):
        # play sound
        self.effects_sounds['loose'].play()
        # set self.playing to True to reset the game
        self.playing = True

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

        # update the camera with the update function and track the player
        self.camera.update(self.player)

        # if player position is bigger than HEIGHT game over
        if self.player.pos.y >= HEIGHT:
            # in the bottom the show gameover screen gets triggered when
            # self.playing is False (the fucntion is empty at the moment)
            self.playing = False

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)

        # here we draw everything with the camera
        self.screen.blit(self.map_img, self.camera.apply(self.map))
        # self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
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
                if event.key == pg.K_p:
                    self.paused = not self.paused
                if event.key == pg.K_n:
                    self.night = not self.night
            if event.type == pg.KEYDOWN:
                 if event.key == pg.K_SPACE:
                     self.player.jump()
                     self.effects_sounds['jump'].play()
                     


    def show_start_screen(self):
        pass

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.died()
    #g.show_go_screen()
