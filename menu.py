import pygame
from datetime import datetime as dt

from debug import debug
from support import import_animations_from_folder, convert_path
from settings import *
from button import Button
from game_stats_settings import *

class Menu:
    def __init__(self, start_game):
        self.visible_sprites = pygame.sprite.Group()
        self.display_suface = pygame.display.get_surface()
        self.buttons = pygame.sprite.Group()

        MenuBackground(self.visible_sprites)

        self.middle_w = self.display_suface.get_width() // 2
        self.middle_h = self.display_suface.get_height() // 2

        self.font_path = convert_path("assets/fonts/PressStart2P.ttf")
        self.font = pygame.font.Font(self.font_path, 20)
        self.font_color = "white"
        self.button_color = "#b3c3d5"

        self.start_game = start_game

        self.create_buttons()

    def set_difficult(self):
        DIFFICULT += 1
        if (DIFFICULT > 1):
            DIFFICULT = -1

    def create_buttons(self):
        Button((self.middle_w, self.middle_h),
                200, 50, 
                "Start", 
                self.button_color, 
                self.font, 
                self.font_color,
                (self.buttons, self.visible_sprites),
                self.start_game)

        Button((self.middle_w, self.middle_h + 100),
                200, 50, 
                "Difficult", 
                self.button_color, 
                self.font, 
                self.font_color,
                (self.buttons, self.visible_sprites),
                gameStats.set_difficult)

    def run(self):
        self.visible_sprites.draw(self.display_suface)
        self.visible_sprites.update()
        debug(gameStats.DIFFICULT)

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
        
        self.animation = import_animations_from_folder(f'assets/sprites/background/Menu/{self.wallpaper}')
        self.anim_index = 0
        self.anim_speed = .045
        self.image = self.animation[0]
        self.rect = self.image.get_rect(topleft = (0,0))
    
    def animate(self):
        self.anim_index += self.anim_speed

        if (self.anim_index > len(self.animation)):
            self.anim_index = 0

        self.image = self.animation[int(self.anim_index)]
        self.rect = self.image.get_rect(topleft = (0, 0))

    def update(self) -> None:
        self.animate()
        