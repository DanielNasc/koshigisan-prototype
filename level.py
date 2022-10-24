import pygame

from Tile import Tile
from camera import YSortCameraGroup
from debug import debug
from player import Player
from settings import *

class Level:
    def __init__(self) -> None:
        self.display_suface = pygame.display.get_surface()

        # setup sprite groups
        self.visible_sprites = YSortCameraGroup() 
        self.obstacle_sprites = pygame.sprite.Group()

        # setup sprite
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(MAP):
            for col_index, data in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE

                if data == "x":
                    Tile((x, y), (self.visible_sprites, self.obstacle_sprites))
                elif data == "p":
                    self.player = Player((x, y), (self.visible_sprites), self.obstacle_sprites)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.direction)
