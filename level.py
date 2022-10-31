import pygame

from Tile import Tile
from camera import YSortCameraGroup
from player import Player
from settings import *
from support import import_positions
from weapon import Weapon

class Level:
    def __init__(self) -> None:
        self.display_suface = pygame.display.get_surface()

        # setup sprite groups
        self.visible_sprites = YSortCameraGroup() 
        self.obstacle_sprites = pygame.sprite.Group()


        self.curr_attack = None

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
                            
                        
        self.player = Player(PLAYER_SPAWN, (self.visible_sprites), self.obstacle_sprites, self.create_attack, self.destroy_attack)

    def create_attack(self):
        self.curr_attack = Weapon(self.player, [self.visible_sprites])
    
    def destroy_attack(self):
        if self.curr_attack:
            self.curr_attack.kill()
        self.curr_attack = None

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
