import pygame
from datetime import datetime as dt

from support.sprites_support import import_animations_from_folder, convert_path, import_a_single_sprite
from settings import *
from level.menu.button import Button
from game_stats_settings import *

from level.menu.guide import *

class Menu:
    def __init__(self, start_game):
        self.visible_sprites = pygame.sprite.Group()
        self.display_suface = pygame.display.get_surface()
        self.buttons = pygame.sprite.Group()

        #lonalt
        self.guid_surface = pygame.sprite.Group()

        MenuBackground(self.visible_sprites)

        
        self.filter = pygame.sprite.Sprite(self.visible_sprites)
        self.filter.image = pygame.surface.Surface((WIDTH, HEIGHT))
        #self.filter.image.convert_alpha()
        self.filter.rect = self.filter.image.get_rect(topleft = (0,0))
        self.filter.image.fill((0,0,0))
        self.filter.image.set_alpha(101) 

        MenuTitle(self.visible_sprites)

        self.middle_w = self.display_suface.get_width() // 2
        self.middle_h = self.display_suface.get_height() // 2

        self.font_path = convert_path("assets/fonts/PressStart2P.ttf")
        self.font = pygame.font.Font(self.font_path, 20)
        self.font_color = "white"
        self.button_color = '#5C8BA8'
        self.button_hover_color = (255, 128, 255, 128)

        self.start_game = start_game

        self.create_buttons()

    def create_guid(self):
        Guid((self.middle_w, self.middle_h),
            900, 300,
            self.create_buttons,
            (self.guid_surface, self.visible_sprites))
        for button in self.buttons:
            button.kill()

    def set_difficult(self):
        DIFFICULT += 1
        if (DIFFICULT > 1):
            DIFFICULT = -1

    def create_buttons(self):
        diff = "Difícil" if gameStats.DIFFICULT == -1 else ("Normal" if gameStats.DIFFICULT == 0 else "Fácil" )
        #screen = "Janela" if pygame.display.get_caption
        Button((self.middle_w, self.middle_h),
                200, 50, 
                "Começar", 
                self.button_color,
                self.font, 
                self.font_color,
                (self.buttons, self.visible_sprites),
                20,  (64, 64, 128, 128), self.button_hover_color,
                self.start_game)

        Button((self.middle_w, self.middle_h + 75),
                200, 50, 
                "Guia", 
                self.button_color,
                self.font, 
                self.font_color,
                (self.buttons, self.visible_sprites),
                20,  (64, 64, 128, 128), self.button_hover_color,
                self.create_guid)

        self.dif = Button((self.middle_w, self.middle_h + 150),
                200, 50, 
                diff, 
                self.button_color,
                self.font, 
                self.font_color,
                (self.buttons, self.visible_sprites),
                20,  (64, 64, 128, 128), self.button_hover_color,
                self.recreate_difficulty_button)

        self.fullsreen_button = Button((self.middle_w, self.middle_h + 225),
                200, 50, 
                "Janela", 
                self.button_color,
                self.font, 
                self.font_color,
                (self.buttons, self.visible_sprites),
                20,  (64, 64, 128, 128), self.button_hover_color,
                self.recreate_fullscreen_button)
        
        Button((self.middle_w, self.middle_h + 300),
                200, 50, 
                "Sair", 
                self.button_color,
                self.font, 
                self.font_color,
                (self.buttons, self.visible_sprites),
                20,  (64, 64, 128, 128), self.button_hover_color,
                gameStats.close)

    def recreate_fullscreen_button(self):
        gameStats.change_screen()
        text = "Tela Cheia" if gameStats.is_fullscreen else "Janela"
        self.fullsreen_button.kill()
        self.fullsreen_button = Button((self.middle_w, self.middle_h + 225),
                200, 50, 
                text, 
                self.button_color,
                self.font, 
                self.font_color,
                (self.buttons, self.visible_sprites),
                20,  (64, 64, 128, 128), self.button_hover_color,
                self.recreate_fullscreen_button)

    def recreate_difficulty_button(self):
        gameStats.set_difficult()
        self.dif.kill()
        diff = "Difícil" if gameStats.DIFFICULT == -1 else ("Normal" if gameStats.DIFFICULT == 0 else "Fácil" )
        self.dif = Button((self.middle_w, self.middle_h + 150),
                200, 50, 
                diff, 
                self.button_color,
                self.font, 
                self.font_color,
                (self.buttons, self.visible_sprites),
                20,  (64, 64, 128, 128), self.button_hover_color,
                self.recreate_difficulty_button)

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

class MenuTitle(pygame.sprite.Sprite):
    def __init__(self, groups) -> None:
        super().__init__(groups)

        width = 1000
        height = 300

        self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA)
        self.image.convert_alpha()
        self.rect = self.image.get_rect(center = (WIDTH // 2, 120))

        self.raw_text = "KOSHIG SAN"
        self.font_path = convert_path("assets/fonts/PressStart2P.ttf")
        self.font = pygame.font.Font(self.font_path, 90)

        self.text = self.font.render(self.raw_text, True, 'white')
        self.text_rect = self.text.get_rect(center=(width // 2, height // 2))
        self.text.convert_alpha()

        # Create a transparent surface.
        alpha_img = pygame.Surface(self.text.get_size(), pygame.SRCALPHA)
        # Fill it with white and the desired alpha value.
        alpha_img.fill((255, 255, 255, 140))
        # Blit the alpha surface onto the text surface and pass BLEND_RGBA_MULT.
        self.text.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        pygame.draw.line(self.image, (255, 255, 255, 140), (0, (height // 2) - 90), (width, (height // 2) - 90), 10)
        pygame.draw.line(self.image, (255, 255, 255, 140), (0, (height // 2) + 70), (width, (height // 2) + 70), 10)


        self.sword = import_a_single_sprite('assets/sprites/background/Title_Sword.png', .8)
        self.sword_pos = (
            630, 140
        )
        self.sword_rect = self.sword.get_rect(center = self.sword_pos)
        self.image.blit(self.text, self.text_rect)
        self.image.blit(self.sword, self.sword_rect)

    