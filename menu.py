import pygame
from camera import YSortCameraGroup
from support import import_animations_from_folder
from settings import *

class Menu:
    def __init__(self, level = None, has_animated_background = False):

        self.visible_sprites = YSortCameraGroup('Menu') 
        self.display_suface = pygame.display.get_surface()
        self.has_animated_background = has_animated_background

    def run(self):
        self.visible_sprites.draw(self.display_suface)
        self.visible_sprites.update()

    def load_background(self,has_animated_background):
        if has_animated_background:
            self.animation = import_animations_from_folder('assets/sprites/background/{self.level}')
            self.anim_index = 0 
            self.floor_surface = self.animation[0]


            