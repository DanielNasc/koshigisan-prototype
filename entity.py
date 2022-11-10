import pygame   
from math import sin


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups) -> None:
        super().__init__(groups)
        self.frame_index = 0
        self.direction = pygame.math.Vector2() 
        self.animation_speed = .15
        
    def move(self, speed: int=10):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        if (self.is_sliding):
            speed *= 1.25

        self.hitbox.x += self.direction.x * speed
        self.detect_collision("horizontal")

        self.hitbox.y += self.direction.y * speed
        self.detect_collision("vertical")

        self.rect.center = self.hitbox.center
    
    def detect_collision(self, direction):

        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # andando para a direita
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0: # andando para a esquerda
                        self.hitbox.left = sprite.hitbox.right
                    self.direction.x = 0

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # andando para baixo
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0: # andando para cima
                        self.hitbox.top = sprite.hitbox.bottom
                    self.direction.y = 0
        
        is_colliding_slippery_sprite = False
        for sprite in self.slippery_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                is_colliding_slippery_sprite = True
                break

        self.is_sliding = is_colliding_slippery_sprite

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0