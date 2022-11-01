import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups)
        # self.image = pygame.image.load("assets/sprites/placeholder.png")
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -(self.rect.height * .6))
        self.sprite_type = sprite_type
