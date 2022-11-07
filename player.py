from math import floor
import pygame
from settings import *
from support import import_sprites
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacles: pygame.sprite.Group, slippery_sprites: pygame.sprite.Group, 
                create_attack, destroy_attack, create_magic):
        super().__init__(groups)

        #### Animação

        # pegar todas as animações dos jogador e colocar na propriedade anim
        self.anim = import_sprites('assets/sprites/characteres/yamato')

        # ajustar o zoom do sprite do player
        for anim_array  in self.anim.values():
            for i in range(len(anim_array)):
                player_size_vector = pygame.math.Vector2(anim_array[i].get_size())
                anim_array[i] = pygame.transform.scale(anim_array[i], player_size_vector * PLAYER_ZOOM)
        
        self.image = self.anim["down_idle"][0]

        self.status = 'down'
        #self.animation_speed = ATTACK_SPEED

        #### Ataques

        self.can_attack = True
        self.can_attack_w_magic = True
        self.is_attacking = False
        self.is_attacking_w_magic = False
        self.is_blocked = False
        self.is_sliding = False
        self.attack_cooldown = 1000
        self.magic_cooldown = 600
        self.attack_time = 0
        self.magic_time = 0
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack

        self.weapon_index = 0
        self.weapon = list(weapons_data.keys())[self.weapon_index]

        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.weapon_index]
        self.create_magic = create_magic
        self.selected_magic = magic_data[self.magic]

        #### Rect

        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10) # Hitbox com altura menor que o rect para possibiltar o efeito de overlay

        self.obstacle_sprites = obstacles
        self.slippery_sprites = slippery_sprites

        #------------- Maluzinha ------------------
        #### Estatísticas
        self.stats = {'health': 100, 'mana': 60, 'attack': 10, 'speed': 2}
        self.health = self.stats['health']
        self.mana = self.stats['mana']
        self.exp = 123 ## teste


    def input(self):
        if self.is_blocked:
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_x] and self.can_attack and not self.is_sliding:
            self.is_attacking = True
            self.can_attack = False
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()

        if keys[pygame.K_z] and self.can_attack and not self.is_sliding:
            self.is_attacking_w_magic = True
            self.can_attack_w_magic = False
            self.magic_time = pygame.time.get_ticks()

            style = list(magic_data.keys())[self.magic_index]
            strength = self.selected_magic["strength"]
            cost = self.selected_magic["cost"]

            self.create_magic(style, strength, cost)

    def cooldown(self):
        curr_time = pygame.time.get_ticks()

        if (curr_time - self.attack_time >= self.attack_cooldown):
            self.is_attacking = False
            self.can_attack = True
            self.destroy_attack()

        if (curr_time - self.magic_time >= self.magic_cooldown):
            self.is_attacking_w_magic = False
            self.can_attack = True

    
    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and "attack" not in self.status and not "magic" in self.status:
                self.status += '_idle'
                self.frame_index = 0

        if self.is_attacking:
            self.direction.x = self.direction.y = 0

            if not "attack" in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("idle", "attack")
                else:
                    self.status += "_attack"
                self.frame_index = 0
                    
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")
                self.frame_index = 0

        if self.is_attacking_w_magic:
            self.direction.x = self.direction.y = 0

            if not "magic" in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("idle", "magic")
                else:
                    self.status += "_magic"
                self.frame_index = 0
                    
        else:
            if "magic" in self.status:
                self.status = self.status.replace("_magic", "")
                self.frame_index = 0
                

    def animate(self):
        if (self.is_sliding): return
        
        animation = self.anim[self.status]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0
            if self.is_attacking:
                self.is_attacking = False
                self.destroy_attack()


        # set the image
        self.image = animation[floor(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update_blocked(self):
        self.is_blocked = self.is_attacking or self.is_attacking_w_magic
        
        if self.is_sliding:
            self.is_blocked = not ( self.direction.x == 0 and self.direction.y == 0 and self.is_sliding )

    def update(self):
        self.cooldown()
        self.update_blocked()
        self.input()
        self.get_status()
        self.animate()
        self.move()