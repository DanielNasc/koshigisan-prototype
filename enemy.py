import pygame
import math

from player import Player
from entity import Entity
from support import import_sprites
from settings import monsters_data

"""
Estagios: [0] Idle, [1] Notar, [2] Preparar, [3] Atacar

[0] Idle: fica parado, esperando o player entrar em seu notice_radius
[1] Notar: Se movimenta quando o player entra em seu notice_radius
[2] Preparar: Fica estático por pouco tempo, dando a ideia de estar se preparando e dando tempo do player se esquivar
[3] Atacar: Efetua o ataque

"""

IDLE = 0
NOTICE = 1
PREPARE = 2
ATTACK = 3

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, slippery_sprites) -> None:
        super().__init__(groups)

        # general
        self.sprite_type = "enemy"
        self.obstacle_sprites = obstacle_sprites
        self.slippery_sprites = slippery_sprites    

        # stats
        self.monster_name = monster_name
        monster_info = monsters_data[monster_name]
        self.health = monster_info["health"]
        self.exp = monster_info["exp"]
        self.damage = monster_info["damage"]
        self.attack_type = monster_info["attack_type"]
        self.speed = monster_info["speed"]
        self.speed_boost = 1
        self.resistance = monster_info["resistance"]
        self.attack_radius = monster_info["attack_radius"]
        self.notice_radius = monster_info["notice_radius"]
        self.scale = monster_info["scale"]
        self.preparing_duration = monster_info["preparing_duration"]
        self.is_sliding = False
 
        # graphics
        self.import_graphics(monster_name)
        self.status = "down_idle"
        self.image = self.anim[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        # movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)

        # player interaction
        self.can_attack = True
        self.is_attacking = False
        self.is_blocked = False
        self.attack_cooldown = 1000
        self.attack_duration = 2000
        self.preparing_time = None
        self.stage = IDLE


    def import_graphics(self, monster_name):
        self.anim = import_sprites(f"assets/sprites/monsters/{self.monster_name}", self.scale)

    def get_player_distance_and_direction(self, player: Player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center) 

        distance = (player_vec - enemy_vec).magnitude()
        direction = (player_vec - enemy_vec).normalize() if distance > 0 else pygame.math.Vector2()

        return (distance, direction)

    # pega o status da animação
    def get_status(self):
        direction = "down"

        if self.stage == ATTACK:
            if "attack" not in self.status:
                self.frame_index = 0
            self.status = direction + "_attack"
        elif self.stage == NOTICE:
            self.status = direction + "_move"
        else:
            self.status = direction + "_idle"

    def actions(self, player):
        if "attack" in self.status:
            self.attack_time = pygame.time.get_ticks()
            
            if self.attack_type == "continuous":
                self.direction = pygame.math.Vector2()
            else:
                self.speed_boost =  2 if self.attack_type == "dash" else 1

        elif "move" in self.status:
            self.direction = self.get_player_distance_and_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def cooldown(self):
        curr_time = pygame.time.get_ticks()

        if not self.can_attack:
            if curr_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
                self.is_attacking = False

        if self.stage == ATTACK:
            if curr_time - self.attack_duration >= self.is_attacking:
                self.stage = IDLE
                self.is_attacking = False

        if self.stage == PREPARE:
            if curr_time - self.preparing_time >= self.preparing_duration:
                self.stage = ATTACK
                self.is_blocked = False
                self.is_attacking = True

    def animate(self):
        if (self.is_sliding): return
        
        animation = self.anim[self.status]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            if self.stage == ATTACK and self.attack_type != "continuous":
                self.can_attack = False
            self.frame_index = 0

        # set the image
        self.image = animation[math.floor(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        if (not self.is_blocked):
            self.move(self.speed * self.speed_boost)
        self.animate()
        self.cooldown()

    def enemy_update(self, player):
        self.get_status()
        self.actions(player)

class ContinuousEnemy(Enemy):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, slippery_sprites) -> None:
        super().__init__(monster_name, pos, groups, obstacle_sprites, slippery_sprites)

    def get_stage(self, player):
        distance, direction = self.get_player_distance_and_direction(player)

        if distance <= self.attack_radius:
            self.stage = ATTACK
        elif distance <= self.notice_radius:
            self.stage = NOTICE
        else:
            self.stage = IDLE

    def actions(self, player):
        if self.stage == ATTACK:
            self.attack_time = pygame.time.get_ticks()
            self.direction = pygame.math.Vector2()
            
        elif "move" in self.status:
            self.direction = self.get_player_distance_and_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def update(self):
        if (not self.is_blocked):
            self.move(self.speed * self.speed_boost)
        self.animate()
        self.cooldown()

    def enemy_update(self, player):
        self.get_stage(player)
        self.get_status()
        self.actions(player)

class DashEnemy(Enemy):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, slippery_sprites) -> None:
        super().__init__(monster_name, pos, groups, obstacle_sprites, slippery_sprites)

    def get_stage(self, player):
        distance, direction = self.get_player_distance_and_direction(player)

        if distance <= self.attack_radius:
            self.stage = ATTACK
        elif distance <= self.notice_radius:
            self.stage = NOTICE
        else:
            self.stage = IDLE

    def actions(self, player):
        self.speed_boost = 1

        if self.stage == ATTACK:
            self.attack_time = pygame.time.get_ticks()
            self.speed_boost = 2
            
        elif "move" in self.status:
            self.direction = self.get_player_distance_and_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def update(self):
        if (not self.is_blocked):
            self.move(self.speed * self.speed_boost)
        self.animate()
        self.cooldown()

    def enemy_update(self, player):
        self.get_stage(player)
        self.get_status()
        self.actions(player)

# if "attack" in self.status:
#             self.attack_time = pygame.time.get_ticks()
            
#             if self.attack_type == "continuous":
#                 self.direction = pygame.math.Vector2()
#             else:
#                 self.speed_boost =  2 if self.attack_type == "dash" else 1

#         elif "move" in self.status:
#             self.direction = self.get_player_distance_and_direction(player)[1]
#         else:
#             self.direction = pygame.math.Vector2()