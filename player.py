import pygame
from settings import *
from support import import_sprites

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles: pygame.sprite.Group):
        super().__init__(groups)

        #### Animação

        # pegar todas as animações dos jogador e colocar na propriedade anim
        self.anim = import_sprites('assets/sprites/characteres/yamato')

        # ajustar o zoom do sprite do player
        for anim_array  in self.anim.values():
            for i in range(len(anim_array)):
                player_size_vector = pygame.math.Vector2(anim_array[i].get_size())
                anim_array[i] = pygame.transform.scale(anim_array[i], player_size_vector * PLAYER_ZOOM)
        
        self.image = self.anim["idle_down"][0]

        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.05

        #### Ataques

        self.is_attacking = False
        self.attack_cooldown = 700
        self.attack_time = 0

        #### Rect

        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10) # Hitbox com altura menor que o rect para possibiltar o efeito de overlay

        self.direction = pygame.math.Vector2() 

        self.obstacle_sprites = obstacles

    def input(self):
        if self.is_attacking:
            self.direction.x = self.direction.y = 0
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

        if keys[pygame.K_x]:
            self.is_attacking = True
            self.attack_time = pygame.time.get_ticks()
            print("sword")

        if keys[pygame.K_z]:
            self.is_attacking = True
            self.attack_time = pygame.time.get_ticks()
            print("magic")

    def cooldown(self):
        curr_time = pygame.time.get_ticks()

        if self.is_attacking and (curr_time - self.attack_time >= self.attack_cooldown):
            self.is_attacking = False
    
    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle_' in self.status:
                self.status = 'idle_' + self.status 
                self.frame_index = 0

    def move(self, speed: int=5):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.detect_collision("horizontal")

        self.hitbox.y += self.direction.y * speed
        self.detect_collision("vertical")

        self.rect.center = self.hitbox.center

    def animate(self):
        animation = self.anim[self.status]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def detect_collision(self, direction):

        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # andando para a direita
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0: # andando para a esquerda
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # andando para baixo
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0: # andando para cima
                        self.hitbox.top = sprite.hitbox.bottom

            

    def update(self):
        self.cooldown()
        self.input()
        self.get_status()
        self.animate()
        self.move()