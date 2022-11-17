from math import floor
import pygame
from settings import *
from support import import_sprites, calculate_property_by_difficult
from entity import Entity
from game_stats_settings import gameStats

class Player(Entity):
    def __init__(self, pos, groups, obstacles: pygame.sprite.Group, slippery_sprites: pygame.sprite.Group,
                interactive_sprites: pygame.sprite.Group,
                create_attack, destroy_attack, create_magic):
        super().__init__(groups)

        #### Animação

        # pegar todas as animações dos jogador e colocar na propriedade anim
        self.anim = import_sprites('assets/sprites/characteres/yamato', PLAYER_ZOOM)
        self.image = self.anim["down_idle"][0]

        self.status = 'down'
        #self.animation_speed = ATTACK_SPEED

        #### Ataques

        self.can_attack = True
        self.can_attack_w_magic = True
        self.can_tp = True
        self.is_attacking = False
        self.is_attacking_w_magic = False
        self.is_blocked = False
        self.is_sliding = False
        self.attack_cooldown = 1000
        self.magic_cooldown = 600
        self.tp_cooldown = 300
        self.tp_time = None
        self.attack_time = 0
        self.magic_time = 0
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.can_interact_with = None
        self.is_dead = False

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
        self.interactive_sprites = interactive_sprites

        #------------- Maluzinha ------------------
        #### Estatísticas
        self.stats = gameStats.player_stats
        self.max_stats = {
                            'health': calculate_property_by_difficult(300), 
                            'mana': calculate_property_by_difficult(140), 
                            'attack': calculate_property_by_difficult(20), 
                            'speed': calculate_property_by_difficult(10), 
                            'magic': calculate_property_by_difficult(10)
                        }

        self.upgrade_cost = {
                                'health': calculate_property_by_difficult(100, True), 
                                'mana': calculate_property_by_difficult(100, True),
                                'attack': calculate_property_by_difficult(100, True), 
                                'speed': calculate_property_by_difficult(100, True), 
                                'magic': calculate_property_by_difficult(100, True)
                            }
        self.mana = self.stats['mana']
        # self.exp = gameStats.player_exp

        #-------------Lonalt-------------------
        # flickering time
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        #import a sound
        self.weapon_attack_sound = pygame.mixer.Sound('assets/SFX/Attack.wav')
        self.teleport_sound = pygame.mixer.Sound('assets/SFX/Teletransport.wav')
        self.weapon_attack_sound.set_volume(0.4)
        self.teleport_sound.set_volume(0.2)

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
            self.weapon_attack_sound.play()

        if keys[pygame.K_z] and self.can_attack and not self.is_sliding:
            self.is_attacking_w_magic = True
            self.can_attack_w_magic = False
            self.magic_time = pygame.time.get_ticks()

            style = list(magic_data.keys())[self.magic_index]
            strength = calculate_property_by_difficult(self.selected_magic["strength"])
            cost = calculate_property_by_difficult(self.selected_magic["cost"], True)

            self.create_magic(style, strength, cost)

        if keys[pygame.K_LSHIFT] and self.can_interact_with:
            if "tp" in self.can_interact_with.sprite_type and self.can_tp:
                self.can_tp = False
                self.tp_time = pygame.time.get_ticks()
                tp_pos = self.can_interact_with.tp_destination_pos
                self.rect.center = self.hitbox.center = tp_pos
                self.teleport_sound.play()

    def cooldown(self):
        curr_time = pygame.time.get_ticks()

        if (curr_time - self.attack_time >= self.attack_cooldown + weapons_data[self.weapon]['cooldown']):
            self.is_attacking = False
            self.can_attack = True
            self.destroy_attack()

        if (curr_time - self.magic_time >= self.magic_cooldown):
            self.is_attacking_w_magic = False
            self.can_attack = True

        if not self.vulnerable:
            if curr_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

        if not self.can_tp:
            if curr_time - self.tp_time >= self.tp_cooldown:
                self.can_tp = True
    
    def get_status(self):
        if self.is_dead:
            self.status = "death_anim"
            return

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
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        if self.is_sliding: return

        animation = self.anim[self.status]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0
            if self.is_attacking:
                self.is_attacking = False
                self.destroy_attack()
            if self.is_dead:
                self.kill()

        # set the image
        self.image = animation[floor(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)



    def update_blocked(self):
        self.is_blocked = self.is_attacking or self.is_attacking_w_magic or self.is_dead
        
        if self.is_sliding:
            self.is_blocked = not ( self.direction.x == 0 and self.direction.y == 0 and self.is_sliding )

    def recovery_mana(self, recovery_value):
        if self.mana < self.stats["mana"]:
            self.mana += recovery_value * self.stats["magic"] 

#----------------Lonalt-------------
    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapons_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def detect_collision(self, direction):
        self.can_interact_with = None
        for sprite in self.interactive_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                self.can_interact_with = sprite
                break
        return super().detect_collision(direction)

    def get_value_by_index(self,index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self,index):
        return list(self.upgrade_cost.values())[index]

    def check_death(self):
        if gameStats.player_health <= 0:
            self.is_dead = True
            self.vulnerable = True

    def update(self):
        self.check_death()
        self.recovery_mana(.007)
        self.cooldown()
        self.update_blocked()
        self.input()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])