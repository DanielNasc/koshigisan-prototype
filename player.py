import pygame
from settings import *
from spritesheet import SpriteSheet

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.spritesheet = SpriteSheet("assets/sprites/SamuraiSpriteSheet.png")
        self.image = self.spritesheet.get_sprite(0, 0, 32, 32)
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2()

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

    def move(self, speed: int=2):
        print(self.direction.magnitude())
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.center += self.direction * speed

    def update(self):
        self.input()
        self.move()