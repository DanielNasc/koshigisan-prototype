from math import floor
import pygame
from os import path
from player import Player
from support import import_animations_from_folder
from settings import ATTACK_SPEED, PLAYER_ZOOM, weapons_data
from game_stats_settings import gameStats

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player: Player, groups) -> None:
        super().__init__(groups)
        self.sprite_type = 'weapon'
        self.direction = player.status.split("_")[0]

        #### graficos

        full_path = path.join(weapons_data[player.weapon]["graphics"], self.direction)
        self.animations = import_animations_from_folder(full_path)
        
        for i in range(len(self.animations)):
                player_size_vector = pygame.math.Vector2(self.animations[i].get_size())
                self.animations[i] = pygame.transform.scale(self.animations[i], player_size_vector * PLAYER_ZOOM)

        self.image = self.animations[0]
        #self.animations = import_sprites("")


        # offset
        self.rect = self.image.get_rect(
                                        center=
                                            player.rect.center 
                                            + pygame.math.Vector2(
                                                                14 * PLAYER_ZOOM * (1 if self.direction != "left" else -1), 0)
                                                                )

        self.index = 0

        
        
    def update(self):
        if self.index >= len(self.animations): return
        self.image = self.animations[floor(self.index)]
        self.index += ATTACK_SPEED * gameStats.dt
