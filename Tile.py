import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups)
        # self.image = pygame.image.load("assets/sprites/placeholder.png")
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        if sprite_type != "house":
            self.hitbox = self.rect.inflate(0, -(self.rect.height * .6))
        else:
            height = self.rect.height
            self.hitbox = pygame.Rect(self.rect.topleft[0], self.rect.topleft[1] + (height * .5), self.rect.width, height * .4)
        self.sprite_type = sprite_type
