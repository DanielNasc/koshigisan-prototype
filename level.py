import pygame

from Tile import Tile
from camera import YSortCameraGroup
from debug import debug
from player import Player
from settings import *
from support import import_positions

class Level:
    def __init__(self) -> None:
        self.display_suface = pygame.display.get_surface()

        # setup sprite groups
        self.visible_sprites = YSortCameraGroup() 
        self.obstacle_sprites = pygame.sprite.Group()

        # setup sprite
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_positions('assets/positions/Sky_Colisões.csv')
        }


        for style,layout in layouts.items():

            for row_index, row in enumerate(layout):
        
                for col_index, data in enumerate(row):
                    if data != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        if style == 'boundary':
                            Tile((x + 490, y), (self.obstacle_sprites), 'invisible')
                            
                        
        self.player = Player(PLAYER_SPAWN, (self.visible_sprites), self.obstacle_sprites)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.status)
