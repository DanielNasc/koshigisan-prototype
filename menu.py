import pygame
from datetime import datetime as dt

from debug import debug
from support import import_animations_from_folder, convert_path
from settings import *
from button import Button
from game_stats_settings import *

from guid import *

class Menu:
    def __init__(self, start_game):
        self.visible_sprites = pygame.sprite.Group()
        self.display_suface = pygame.display.get_surface()
        self.buttons = pygame.sprite.Group()

        #lonalt
        self.guid_surface = pygame.sprite.Group()

        MenuBackground(self.visible_sprites)

        self.middle_w = self.display_suface.get_width() // 2
        self.middle_h = self.display_suface.get_height() // 2

        self.font_path = convert_path("assets/fonts/PressStart2P.ttf")
        self.font = pygame.font.Font(self.font_path, 20)
        self.font_color = "white"
        self.button_color = '#5391c7'
        self.button_backgound_color = '#000000'

        self.start_game = start_game

        self.create_buttons()

    def create_guid(self):
        Guid((self.middle_w, self.middle_h),
            500, 200,
            (self.guid_surface, self.visible_sprites))

    def set_difficult(self):
        DIFFICULT += 1
        if (DIFFICULT > 1):
            DIFFICULT = -1


    def create_buttons(self):
        Button((self.middle_w, self.middle_h),
                200, 50, 
                "Start", 
                self.button_color,
                self.button_backgound_color, 
                self.font, 
                self.font_color,
                (self.buttons, self.visible_sprites),
                self.start_game)

        Button((self.middle_w, self.middle_h + 75),
                200, 50, 
                "Guid", 
                self.button_color,
                self.button_backgound_color,  
                self.font, 
                self.font_color,
                (self.buttons, self.visible_sprites),
                self.create_guid)
        
        Button((self.middle_w, self.middle_h + 150),
                200, 50, 
                "Difficult", 
                self.button_color,
                self.button_backgound_color,  
                self.font, 
                self.font_color,
                (self.buttons, self.visible_sprites),
                gameStats.set_difficult)

        Button((self.middle_w, self.middle_h + 225),
                200, 50, 
                "Exit", 
                self.button_color,
                self.button_backgound_color,  
                self.font, 
                self.font_color,
                (self.buttons, self.visible_sprites),
                gameStats.close)

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
        