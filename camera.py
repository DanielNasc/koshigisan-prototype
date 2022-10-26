import pygame

from player import Player
from settings import HEIGHT, WIDTH

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
        self.offset = pygame.math.Vector2()

        self.half_w = self.display_surface.get_width() // 2
        self.half_h = self.display_surface.get_height() // 2

        self.internal_surf_size = (WIDTH, HEIGHT)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_surf_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_rect = self.internal_surf.get_rect()

    def custom_draw(self, player: Player):
        self.offset.x = player.rect.centerx - self.half_w
        self.offset.y = player.rect.centery - self.half_h

        self.internal_surf.fill((0, 0, 0))

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.y):
            offset_pos = sprite.rect.topleft - self.offset
            self.internal_surf.blit(sprite.image, offset_pos)

        scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surf_size_vector * 2.5)
        scaled_rect = scaled_surf.get_rect(center = (self.half_w, self.half_h))

        self.display_surface.blit(scaled_surf, scaled_rect)