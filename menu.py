import pygame
from datetime import datetime as dt
from camera import YSortCameraGroup
from support import import_animations_from_folder
from settings import *

class Menu:

    def __init__(self):
        self.visible_sprites = pygame.sprite.Group()
        self.display_suface = pygame.display.get_surface()
        MenuBackground(self.visible_sprites)

    def run(self):
        self.visible_sprites.draw(self.display_suface)
        self.visible_sprites.update()

class MenuBackground(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)

        hour = dt.now().hour

        if hour < 12:
            self.wallpaper = 'Morning'
        elif hour >= 12 and hour < 18:
            self.wallpaper = 'Afternoon'
        else:
            self.wallpaper = 'Night'
        
        self.animation = import_animations_from_folder(f'assets/sprites/backgroung/Menu/{self.wallpaper}')
        self.anim_index = 0
        self.image = self.animation[0]
        self.rect = self.image.get_rect(topleft = (0,0))







            