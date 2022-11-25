import pygame
from support.sprites_support import convert_path

class SpriteSheet:
    def __init__(self, filepath: str):
        self.path = convert_path(filepath)
        self.sprite_sheet = pygame.image.load(filepath).convert()

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))

        return sprite

    def get_all(self,w,h):
        sprite_sheet_width = self.sprite_sheet.get_width()
        sprite_sheet_height = self.sprite_sheet.get_height()

        sprites = []
        for x in range(sprite_sheet_width//w):
            for y in range(sprite_sheet_height//h):
                sprites.append(self.get_sprite(x,y,w,h))
        
        return sprites
