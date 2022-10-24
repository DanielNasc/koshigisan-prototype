import pygame

from player import Player

"""
as principais funções dos grupos são

1. armazenar e desenhar sprites
2. chamar o metódo update

mas você pode mudar adicionar novos metodos ou mudar os existentes extendendo a classe
"""

class YSortCameraGroup(pygame.sprite.Group): # extendendo a classe Group
    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.half_w = self.display_surface.get_width() // 2
        self.half_h = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player: Player):
        self.offset.x = player.rect.centerx - self.half_w
        self.offset.y = player.rect.centery - self.half_h

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)