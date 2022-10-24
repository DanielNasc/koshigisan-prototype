import pygame
from settings import *
from spritesheet import SpriteSheet

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles: pygame.sprite.Group):
        super().__init__(groups)
        self.spritesheet = SpriteSheet("assets/sprites/SamuraiSpriteSheet.png")
        self.image = self.spritesheet.get_sprite(0, 0, 32, 32)
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2()

        self.obstacle_sprites = obstacles

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def move(self, speed: int=5):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * speed
        self.detect_collision("horizontal")

        self.rect.y += self.direction.y * speed
        self.detect_collision("vertical")

    def detect_collision(self, direction):

        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0: # andando para a direita
                        self.rect.right = sprite.rect.left
                    elif self.direction.x < 0: # andando para a esquerda
                        self.rect.left = sprite.rect.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0: # andando para baixo
                        self.rect.bottom = sprite.rect.top
                    elif self.direction.y < 0: # andando para cima
                        self.rect.top = sprite.rect.bottom

            

    def update(self):
        self.input()
        self.move()