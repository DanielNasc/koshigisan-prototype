from math import floor
import pygame
from os import path
from entities.player.player import Player
from support.sprites_support import import_animations_from_folder, import_a_single_sprite
from settings import ATTACK_SPEED, PLAYER_ZOOM, weapons_data

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

        hitbox_surface = import_a_single_sprite('assets/masks/quarter_circle.png', .075)
        
        # a imagem está apontando para a direita, então é preciso rotacionar
        offset = 5
        if self.direction == 'left':
            hitbox_surface = pygame.transform.rotate(hitbox_surface, 180)
            hitbox_rect = hitbox_surface.get_rect(
                midright = (player.rect.midleft[0] + offset, player.rect.midleft[1])
            )
        elif self.direction == 'up':
            hitbox_surface = pygame.transform.rotate(hitbox_surface, 90)
            hitbox_rect = hitbox_surface.get_rect(
                midbottom = (player.rect.midtop[0], player.rect.midtop[1] + offset + 5)
            )
        elif self.direction == 'down':
            hitbox_surface = pygame.transform.rotate(hitbox_surface, -90)
            hitbox_rect = hitbox_surface.get_rect(
                midtop = (player.rect.midbottom[0], player.rect.midbottom[1] - offset)
            )
        else:
            hitbox_rect = hitbox_surface.get_rect(
                midleft = (player.rect.midright[0] - offset, player.rect.midright[1])
            )

        self.hitbox_sprite = pygame.sprite.Sprite()
        self.hitbox_sprite.mask = pygame.mask.from_surface(hitbox_surface)
        self.hitbox_sprite.image = hitbox_surface
        self.hitbox_sprite.rect = hitbox_rect
        
    def update(self):
        if self.index >= len(self.animations): return
        self.image = self.animations[floor(self.index)]
        self.index += ATTACK_SPEED
