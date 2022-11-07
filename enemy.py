import pygame
from math import floor

from player import Player
from entity import Entity
from support import import_sprites
from settings import monsters_data

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
        self.attack_cooldown = 10000

    def import_graphics(self, monster_name):
        self.anim = import_sprites(f"assets/sprites/monsters/{self.monster_name}", self.scale)

    def get_player_distance_and_direction(self, player: Player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center) 

        distance = (player_vec - enemy_vec).magnitude()
        direction = (player_vec - enemy_vec).normalize() if distance > 0 else pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player: Player):
        distance = self.get_player_distance_and_direction(player)[0]
        direction = "down"

        if (distance <= self.attack_radius and self.can_attack) or self.is_attacking:
            if "attack" not in self.status:
                self.frame_index = 0
            self.status = direction + "_attack"
        elif distance <= self.notice_radius:
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
        if not self.can_attack:
            curr_time = pygame.time.get_ticks()
            if curr_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
                self.is_attacking = False

    def animate(self):
        if (self.is_sliding): return
        
        animation = self.anim[self.status]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            if "attack" in self.status and self.attack_type != "continuous":
                self.can_attack = False
            self.frame_index = 0

        # set the image
        self.image = animation[floor(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.move(self.speed * self.speed_boost)
        self.animate()
        self.cooldown()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)