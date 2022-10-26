import pygame

class SpriteSheet:
    def __init__(self, filepath: str):
        self.path = filepath
        self.sprite_sheet = pygame.image.load(filepath).convert()

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))

        return sprite
