import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 640  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Binary Bastards Production"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_IMG = 'snow.png'

PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)

# settings from platformer
PLAYER_ACC = 1
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Sounds
BG_MUSIC = ''


EFFECTS_SOUNDS = {'jump': 'jump.wav',
                  'loose': 'loose.wav'}
