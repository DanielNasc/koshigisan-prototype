import pygame
from settings import *
from entities.player.player import Player
from visual.particles import AnimationController
from random import randint
from entities.tile import Tile

class PlayerMagic:
    def __init__(self, animation_controller: AnimationController =None, obstacle_sprites: pygame.sprite.Group =None) -> None:
        self.animation_controller = animation_controller
        self.obstacle_sprites = obstacle_sprites
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

            boundaries = self.obstacle_sprites.sprites()

            for i in range(1, 6):
                if direction.x: # horizontal
                    off_set = direction.x * i * TILESIZE
                    x = player.rect.centerx + off_set + randint(- TILESIZE // 3, TILESIZE // 3 )
                    y = player.rect.centery + randint(- TILESIZE // 3, TILESIZE // 3 )

                    particle = self.animation_controller.create_particles("flame", (x, y), groups)

                    # pegar o boundary que está colidindo com a magia, se houver
                    boundary = None

                    for b in boundaries:
                        if pygame.sprite.collide_rect(particle, b):
                            boundary = b
                            break
                    
                    # checar se o boundary estiver na direção oposta da magia
                    # ela não deve passar

                    brk = False
                    if boundary:
                        # checa se existe um tile em cima ou em baixo do boundary
                        for tile in self.obstacle_sprites:
                            if tile.rect.centerx == boundary.rect.centerx:
                                if tile.rect.centery == boundary.rect.centery + TILESIZE or tile.rect.centery == boundary.rect.centery - TILESIZE:
                                    particle.kill()
                                    brk = True
                                    break
                    if brk: break

                else: # vertical
                    off_set = direction.y * i * TILESIZE
                    x = player.rect.centerx + randint(- TILESIZE // 3, TILESIZE // 3 )
                    y = player.rect.centery + off_set + randint(- TILESIZE // 3, TILESIZE // 3 )

                    particle = self.animation_controller.create_particles("flame", (x, y), groups)
                    
                    # pegar o boundary que está colidindo com a magia, se houver
                    boundary = None

                    for b in boundaries:
                        if pygame.sprite.collide_rect(particle, b):
                            boundary = b
                            break

                    # checar se o boundary estiver na direção oposta da magia
                    # ela não deve passar

                    brk = False
                    if boundary:
                        # checa se existe um tile em cima ou em baixo do boundary
                        for tile in self.obstacle_sprites:
                            if tile.rect.centery == boundary.rect.centery:
                                if tile.rect.centerx == boundary.rect.centerx + TILESIZE or tile.rect.centerx == boundary.rect.centerx - TILESIZE:
                                    particle.kill()
                                    brk = True
                                    break
                    if brk: break

    def heal(self):
        pass