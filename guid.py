import pygame
from settings import *
from button import Button

class Guid(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, restore_buttons, groups):
        super().__init__(groups)
        
        self.pos = pos
        self.font_path = convert_path("assets/fonts/PressStart2P.ttf")
        self.font = pygame.font.Font(self.font_path, 15)
        self.close_button = pygame.sprite.Group()
        self.visible_sprites = pygame.sprite.Group()
        self.width = width
        self.height = height

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, '#252525', (0, 0, width, height), border_radius=20)
        pygame.draw.rect(self.image, '#000000', (0, 0, width, height), width = 4, border_radius=20)
        self.image.set_alpha(220)

        self.get_text()
        self.rect = self.image.get_rect(center=pos)

        self.restore_buttons = restore_buttons

        button_pos =  (
            self.rect.bottomright[0] - 50,
            self.rect.bottomright[1]
        )

        Button(button_pos,
                100, 50, 
                "Close", 
                "#C7424F",
                self.font, 
                "white",
                (self.close_button, self.visible_sprites),
                20,  (64, 64, 128, 128), "#000000",
                self.close)


    def get_text(self):
        Press_M = "Press M to open XP windows"
        Press_Space = "Press Space to buy upgrade"
        Press_X = "Press X to Sword Attack"
        Press_Z = "Press Z to Casting Mage"
        self.create_text(Press_M,2)
        self.create_text(Press_Space,4) 
        self.create_text(Press_X,6)
        self.create_text(Press_Z,8)


    def create_text(self, text, text_pos):
        self.text = self.font.render(text, True, 'white')
        self.text_rect = self.text.get_rect(topleft=(self.width // 10, 10 + self.height // 10 * text_pos))
        self.image.blit(self.text, self.text_rect)

    def close(self):
        for button in self.close_button:
            button.kill()
        self.kill()
        self.restore_buttons()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        self.visible_sprites.update()

        # if self.rect.collidepoint(mouse_pos):
        #     if mouse_pressed[0]:
        #         self.kill()