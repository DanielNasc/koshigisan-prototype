import pygame
from settings import *
from player import Player
from particles import AnimationController
from random import randint

class PlayerMagic:
    def __init__(self, animation_controller: AnimationController =None) -> None:
        self.animation_controller = animation_controller
        self.sounds = {
            'flame': pygame.mixer.Sound('assets/SFX/Magia_de_fogo.wav')
            }
    
    def flame(self, player: Player, cost, groups):
        if player.mana >= cost:
            player.mana -= cost
            self.sounds['flame'].play()

            player_dir = player.status.split("_")[0]

            if player_dir == "down": direction = pygame.math.Vector2(0, 1)
            elif player_dir == "up": direction = pygame.math.Vector2(0, -1)
            elif player_dir == "left":  direction = pygame.math.Vector2(-1, 0)
            else:  direction = pygame.math.Vector2(1, 0)

            for i in range(1, 6):
                if direction.x: # horizontal
                    off_set = direction.x * i * TILESIZE
                    x = player.rect.centerx + off_set + randint(- TILESIZE // 3, TILESIZE // 3 )
                    y = player.rect.centery + randint(- TILESIZE // 3, TILESIZE // 3 )

                    self.animation_controller.create_particles("flame", (x, y), groups)
                else: # vertical
                    off_set = direction.y * i * TILESIZE
                    x = player.rect.centerx + randint(- TILESIZE // 3, TILESIZE // 3 )
                    y = player.rect.centery + off_set + randint(- TILESIZE // 3, TILESIZE // 3 )

                    self.animation_controller.create_particles("flame", (x, y), groups)

    def heal(self):
        pass