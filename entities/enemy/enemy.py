import pygame
import math

from entities.player.player import Player
from entities.entity import Entity

from support.sprites_support import *
from game_stats_settings import gameStats

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
    def __init__(self, monster_name, pos, groups, obstacle_sprites, slippery_sprites, damage_player, trigger_death_particles, add_exp) -> None:
        super().__init__(groups)

        # general
        self.angle = 0
        self.sprite_type = "enemy"
        self.obstacle_sprites = obstacle_sprites
        self.slippery_sprites = slippery_sprites    

        # stats
        self.monster_name = monster_name
        monster_info = monsters_data[monster_name]
        self.health = gameStats.calculate_property_by_difficult(monster_info["health"], True)
        self.exp = gameStats.calculate_property_by_difficult(monster_info["exp"])
        self.damage = gameStats.calculate_property_by_difficult(monster_info["damage"], True)
        self.attack_type = monster_info["attack_type"]
        self.speed = monster_info["speed"]
        self.speed_boost = 1
        self.resistance = gameStats.calculate_property_by_difficult(monster_info["resistance"], True)
        self.attack_radius = monster_info["attack_radius"]
        self.notice_radius = monster_info["notice_radius"]
        self.scale = monster_info["scale"]
        self.preparing_duration = monster_info["preparing_duration"]
        self.is_sliding = False
 
        # graphics
        self.import_graphics(monster_name)
        self.status = "down_idle"
        self.image = self.anim[self.status][self.frame_index]
        self.sprite_dir = "down"

        # movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)

        # player interaction
        self.can_attack = True
        self.is_blocked = False
        self.is_preparing = False
        self.attack_cooldown = 1000
        self.attack_duration = 2000
        self.preparing_time = None
        self.stage = IDLE
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp

#----------DevLonalt---------
        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300
        
        #sounds
        self.death_sound = pygame.mixer.Sound('assets/SFX/Death.wav')
        self.hit_sound = pygame.mixer.Sound('assets/SFX/Hit_Hurt_P.wav')
        self.attck_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.death_sound.set_volume(0.2)
        self.hit_sound.set_volume(0.3)
        self.attck_sound.set_volume(0.3)

    def import_graphics(self,monster_name):
        self.anim = import_sprites(f"assets/sprites/monsters/{self.monster_name}", self.scale)

    def get_player_distance_and_direction(self, player: Player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        
        xp = player.rect.centerx 
        xe = self.rect.centerx
        yp = - player.rect.centery
        ye = - self.rect.centery

        angle = math.degrees(math.atan2(ye - yp, xe -xp)) % 360

        distance = (player_vec - enemy_vec).magnitude()
        direction = (player_vec - enemy_vec).normalize() if distance > 0 else pygame.math.Vector2()

        return (distance, direction, angle)

    def get_direction(self, player):
        _, _, angle = self.get_player_distance_and_direction(player)
        self.angle = angle

        if angle <= 45 or angle >= 315:
            self.sprite_dir = "left"
        elif angle > 45 and angle <= 135:
            self.sprite_dir = "down"
        elif angle > 135 and angle <= 225:
            self.sprite_dir = "right"
        else:
            self.sprite_dir = "up"
        

    # pega o status da animação
    def get_status(self):
        if self.stage == ATTACK:
            if "attack" not in self.status:
                self.frame_index = 0
            self.status = self.sprite_dir + "_attack"
        elif self.stage == NOTICE:
            self.status = self.sprite_dir + "_move"
        else:
            self.status = self.sprite_dir + "_idle"

    def actions(self, player):
        if "attack" in self.status:
            self.attack_time = pygame.time.get_ticks()
            if self.attack_type == "continuous":
                self.direction = pygame.math.Vector2()
            else:
                self.speed_boost = 3 if self.attack_type == "dash" else 1
        elif "move" in self.status:
            self.direction = self.get_player_distance_and_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def cooldowns(self):
        curr_time = pygame.time.get_ticks()

        if not self.can_attack:
            if curr_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if self.stage == ATTACK:
            if curr_time - self.attack_time >= self.attack_duration:
                self.stage = IDLE

        if self.stage == PREPARE:
            if curr_time - self.preparing_time >= self.preparing_duration:
                self.stage = ATTACK
                self.is_blocked = self.is_preparing = False
                # self.attack_time
        if not self.vulnerable:
            if curr_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.anim[self.status]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            if self.stage == ATTACK and self.attack_type != "continuous":
                self.can_attack = False
            self.frame_index = 0

        # set the image
        self.image = animation[math.floor(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # flickering image
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

#--------------Lonalt--------
    def get_damage(self, player: Player,attack_type):
        if self.vulnerable:
            self.hit_sound.play()
            self.direction = self.get_player_distance_and_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            elif attack_type == 'magic':
                self.health -= player.get_full_magic_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            gameStats.enemies_amount -= 1
            self.kill()
            self.trigger_death_particles(self.rect.center,self.monster_name)
            self.add_exp(self.exp)
            self.death_sound.play()
            gameStats.player_health += 5
            if gameStats.player_health > gameStats.player_stats["health"]:
                gameStats.player_health = gameStats.player_stats["health"]
    
    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        if (not self.is_blocked):
            self.move(self.speed * self.speed_boost)
        self.animate()
        self.cooldowns()

    def enemy_update(self, player):
        self.get_status()
        self.actions(player)
        self.get_direction(player)


"""

Inimigo com ataque Continuo (Nukekubi)
Não tem o Stage de preparação

"""


class ContinuousEnemy(Enemy):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, slippery_sprites, damage_player, trigger_death_particles, add_exp) -> None:
        super().__init__(monster_name, pos, groups, obstacle_sprites, slippery_sprites, damage_player, trigger_death_particles, add_exp)

    def get_stage(self, player):
        distance = self.get_player_distance_and_direction(player)[0]

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
            self.damage_player(self.damage,self.attack_type)
            self.attck_sound.play()
        elif "move" in self.status:
            self.direction = self.get_player_distance_and_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def update(self):
        self.hit_reaction()
        if (not self.is_blocked):
            self.move(self.speed * self.speed_boost)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player):
        self.get_direction(player)
        self.get_stage(player)
        self.get_status()
        self.actions(player)

"""
Inimigo com ataque de Dash (Águia)
"""

class DashEnemy(Enemy):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, slippery_sprites, damage_player, trigger_death_particles, add_exp) -> None:
        super().__init__(monster_name, pos, groups, obstacle_sprites, slippery_sprites, damage_player,  trigger_death_particles, add_exp)
        self.can_apply_damage = True
    
    def detect_collision(self, direction, player: Player = None):
        if (player):
            if(player.hitbox.colliderect(self.hitbox) and self.can_apply_damage):
                self.damage_player(self.damage,self.attack_type)
                self.attck_sound.play()
                self.can_apply_damage = False
            else:
                self.can_apply_damage = True
        return super().detect_collision(direction)

    def get_stage(self, player):
        distance = self.get_player_distance_and_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.stage != ATTACK:
                self.stage = PREPARE
        elif distance <= self.notice_radius:
            self.is_preparing = self.is_blocked = False
            self.stage = NOTICE 
        else:
            self.is_preparing = self.is_blocked = False
            self.stage = IDLE

    def actions(self, player):
        self.speed_boost = 1

        if self.stage == ATTACK:
            self.attack_time = pygame.time.get_ticks()
            self.speed_boost = 3

        elif self.stage == PREPARE:
            if (self.is_preparing):
                return

            self.preparing_time = pygame.time.get_ticks()
            self.is_blocked = self.is_preparing = True

        elif "move" in self.status:
            self.direction = self.get_player_distance_and_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()


    def update(self):
        self.hit_reaction()
        if (not self.is_blocked):
            self.move(self.speed * self.speed_boost)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player):
        self.get_direction(player)
        self.detect_collision(self.direction, player)
        self.get_stage(player)
        self.get_status()
        self.actions(player)
