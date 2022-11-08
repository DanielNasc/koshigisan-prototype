from random import choice
import pygame

from Tile import Tile
from camera import YSortCameraGroup
from player import Player
from settings import *
from support import import_animations_from_folder, import_positions
from weapon import Weapon
from ui import UI
from enemy import *

class Level:
    def __init__(self) -> None:
        self.display_suface = pygame.display.get_surface()

        # setup sprite groups
        self.visible_sprites = YSortCameraGroup() 
        self.obstacle_sprites = pygame.sprite.Group()
        self.slippery_sprites = pygame.sprite.Group()
        self.enemies_sprites = pygame.sprite.Group()

        self.curr_attack = None

        # setup sprite
        self.create_map()

        # -------------- Maluzinha ------------
        # user interface
        self.ui = UI()

    def create_map(self):
        layouts = {
            'boundary': import_positions('assets/positions/Skymap_FloorBlocks.csv'),
            'grass': import_positions('assets/positions/Skymap_Grass.csv'),
            'tree': import_positions('assets/positions/Skymap_Trees.csv'),
            'tree2': import_positions('assets/positions/Skymap_Trees2.csv'),
            'ice': import_positions('assets/positions/Skymap_Water.csv'),
            'entities': import_positions('assets/positions/Spawn_Positions.csv')
        }

        graphics = {
            'grass': import_animations_from_folder("assets/sprites/grass"),
            'trees': import_animations_from_folder("assets/sprites/trees")
        }

        for style,layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, data in enumerate(row):
                    if data != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        if style == 'boundary':
                            Tile((x, y), (self.obstacle_sprites), 'invisible')

                        elif style == 'grass':
                            random_grass = choice(graphics['grass'])
                            grass_size =  pygame.math.Vector2(random_grass.get_size())
                            random_grass = pygame.transform.scale(random_grass, grass_size * .5)
                            random_grass.get_rect(center=random_grass.get_rect().midbottom)
                            Tile((x, y), (self.visible_sprites), 'grass', random_grass)

                        elif (style == "tree" or style == "tree2") and data == "t":
                            random_tree = choice(graphics["trees"])
                            Tile((x, y), (self.visible_sprites, self.obstacle_sprites), 'tree', random_tree)

                        elif style == "ice":
                            Tile((x, y), (self.slippery_sprites), 'ice')
                        
                        elif style == "entities":
                            if data == "p":
                                self.player = Player(
                                        (x, y),
                                        (self.visible_sprites),
                                        self.obstacle_sprites,
                                        self.slippery_sprites,
                                        self.create_attack,
                                        self.destroy_attack,
                                        self.create_magic
                                    )
                            elif data == "14":
                                DashEnemy("eagle", (x, y), [self.visible_sprites], self.obstacle_sprites, self.slippery_sprites)
                            else:
                                ContinuousEnemy("nukekubi", (x, y), [self.visible_sprites], self.obstacle_sprites, self.slippery_sprites)

    def create_attack(self):
        self.curr_attack = Weapon(self.player, [self.visible_sprites])

    def create_magic(self, style, strength, cost):
        pass
    
    def destroy_attack(self):
        if self.curr_attack:
            self.curr_attack.kill()
        self.curr_attack = None

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)

        # -------------- Maluzinha ---------
        self.ui.display(self.player)
