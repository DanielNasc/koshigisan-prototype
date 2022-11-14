import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups)
        # self.image = pygame.image.load("assets/sprites/placeholder.png")
        self.image = surface

        if sprite_type == "torii_right":
            pos = (pos[0] - 16, pos[1])
    
        self.rect = self.image.get_rect(topleft = pos)

        if "ladder" in sprite_type:
            self.hitbox = self.rect
        elif "torii" in sprite_type:
            self.hitbox = self.rect.inflate(-(self.rect.height * .6), -(self.rect.height * .6))
        elif sprite_type == "ice_down":
            self.hitbox = self.rect.inflate(0, (self.rect.height * 1.2))
        elif sprite_type == "tree":
            self.hitbox = self.rect.inflate(0, -(self.rect.height * .4))
        elif "entrie" in sprite_type:
            self.hitbox = self.rect.inflate(0, -(self.rect.height * .4)) 
        elif sprite_type != "house":
            self.hitbox = self.rect.inflate(0, -(self.rect.height * .6))
        else:
            height = self.rect.height
            self.hitbox = pygame.Rect(self.rect.topleft[0], self.rect.topleft[1] + (height * .5), self.rect.width, height * .4)
        self.sprite_type = sprite_type

class Teleporter(Tile):
    def __init__(self, pos, groups, sprite_type, direction, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(pos, groups, sprite_type, surface)
        self.direction = direction

        x = self.rect.centerx + (32 * self.direction[0])
        y = self.rect.centery + (32 * self.direction[1])

        self.my_tp_pos = self.tp_destination_pos = (x, y)


    # update teleport pos
    def update_tp_destination(self, tp_destination_pos):
        self.tp_destination_pos = tp_destination_pos
