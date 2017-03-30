import pygame as pg
from random import uniform, choice, randint, random
from settings import *
from tiledmap import collide_hit_rect

vec = pg.math.Vector2


# funktionen har parametre som udgør sprite og group som kan collides
# og i en retning (fx x).
def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        # hvis x retning: hits er lig parametre, hvor
        # sprite og group collides ved metoden collide_hit_rect
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        # if hits is true
        if hits:
            # tjek op på dette afsnit
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y



class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        mediator = None
        self._layer = PLAYER_LAYER
        # bliver en del af alle sprite
        self.groups = game.all_sprites
        # initialisere Player med pygame Sprite
        pg.sprite.Sprite.__init__(self, self.groups)
        # Player bliver tildelt nedenstående funktionaliteter
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # får tildelt en værdi som udgør hans collide rect. 35 * 35
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        # Players velocity, position og acc.
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)  # x and PLAYER_GRAV makes the player move downwards (gravity)
        # checker om der er blevet tastet paa en tast

        # vores rect rykkes 5 pixel til hoejre eller venstre naar pilenetasterne bruges
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        # her laves fysike love til player
        # apply friction
        # .x sets friction on the x axis only (so we accelerete when falling)
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # acceleration
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # set to midbottom so we can stand on the platforms
        self.rect.midbottom = self.pos
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        # kalder metoden fra anden class
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def jump(self):
        # jump only if standing on platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        self.rect.x -= 1
        # hvis hits velocity y = -14
        if hits:
            self.vel.y = -14
