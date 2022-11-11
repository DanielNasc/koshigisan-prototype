from random import choice
import pygame

from Tile import Tile
from camera import YSortCameraGroup
from player import Player
from settings import *
from support import import_animations_from_folder, import_positions, import_a_single_sprite
from weapon import Weapon
from ui import UI
from enemy import *
from particles import AnimationController

class Level:
    def __init__(self, curr_level) -> None:
        self.display_suface = pygame.display.get_surface()

        # Levels
        self.curr_level = curr_level

        # setup sprite groups
        self.visible_sprites = YSortCameraGroup(self.curr_level) 
        self.obstacle_sprites = pygame.sprite.Group()
        self.slippery_sprites = pygame.sprite.Group()
        self.enemies_sprites = pygame.sprite.Group()

        # attack sprites
        self.curr_attack = None
        #---------------Lonalt-------------------
        self.attack_sprites = pygame.sprite.Group()
        self.attackble_sprites = pygame.sprite.Group()

        # setup sprite
        self.create_layouts()
        self.create_map()

        # -------------- Maluzinha ------------
        # user interface
        self.ui = UI()

        # particles
        self.animation_controller = AnimationController()

    def create_layouts(self):
        self.layouts = {
            'boundary': import_positions(f'assets/positions/{self.curr_level}/{self.curr_level}map_FloorBlocks.csv'),
            'entities': import_positions(f'assets/positions/{self.curr_level}/Spawn_Positions.csv')
        }

        if (self.curr_level == "Sky"):
            self.layouts.update({
                'grass': import_positions('assets/positions/Sky/Skymap_Grass.csv'),
                'tree': import_positions('assets/positions/Sky/Skymap_Trees.csv'),
                'tree2': import_positions('assets/positions/Sky/Skymap_Trees2.csv'),
                'ice': import_positions('assets/positions/Sky/Skymap_Water.csv'),
                'house': import_positions('assets/positions/Sky/Skymap_Houses.csv')
            })
        # elif (self.curr_level == "Hell"):
        #     self.layouts.update({

        #     })

    def create_map(self):

        graphics = {
            'grass': import_animations_from_folder("assets/sprites/grass"),
            'trees': import_animations_from_folder("assets/sprites/trees"),
            'houses': import_animations_from_folder("assets/sprites/houses")
        }

        for style,layout in self.layouts.items():
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
                                DashEnemy("eagle", (x, y), [self.visible_sprites,self.attackble_sprites], self.obstacle_sprites, self.slippery_sprites,self.damage_player)
                            elif data == "A":
                                akuma = import_a_single_sprite('assets/sprites/monsters/akuma_front.png', 2)
                                Tile((x, y), [self.visible_sprites], 'boss', akuma)
                            else:
                                ContinuousEnemy("nukekubi", (x, y), [self.visible_sprites,self.attackble_sprites], self.obstacle_sprites, self.slippery_sprites,self.damage_player)

                        elif style == "house":
                            house = None
                            if (data == "gr"):
                                house = import_a_single_sprite('assets/sprites/houses/gr.png')
                            elif (data == "gb"):
                                house = import_a_single_sprite('assets/sprites/houses/gb.png')
                            elif (data == "gn"):
                                house = import_a_single_sprite('assets/sprites/houses/gn.png', 1.2)
                            elif (data == "sn"):
                                house = import_a_single_sprite('assets/sprites/houses/sn.png', 1.5)
                            elif (data == "sn2"):
                                house = import_a_single_sprite('assets/sprites/houses/sn2.png', 1.5)
                            elif (data == "n"):
                                house = import_a_single_sprite('assets/sprites/houses/n.png',1.2)
                            elif (data == "k"):
                                house = import_a_single_sprite('assets/sprites/houses/koshigi.png')
                            elif (data == "b"):
                                house = import_a_single_sprite('assets/sprites/houses/budah.png')

                            if (house):
                                Tile((x, y), (self.visible_sprites, self.obstacle_sprites), 'house', house)

    def create_attack(self):
        self.curr_attack = Weapon(self.player, [self.visible_sprites,self.attack_sprites])

    def create_magic(self, style, strength, cost):
        pass
    
    def destroy_attack(self):
        if self.curr_attack:
            self.curr_attack.kill()
        self.curr_attack = None

    #--------------Lonalt-------------------
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprites in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprites,self.attackble_sprites,False)
                if collision_sprites:
                    for target_sprit in collision_sprites:
                        target_sprit.get_damage(self.player,attack_sprites.sprite_type)

    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            # spawn particles



    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)

        #---------------Lonalt------------
        self.player_attack_logic()

        # -------------- Maluzinha ---------
        self.ui.display(self.player)
