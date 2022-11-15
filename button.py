import pygame 
from game_stats_settings import *

class Button(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, text, color, font, text_color, groups, action=None):
        super().__init__(groups)

        # button with rounded corners
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, color, (0, 0, width, height), border_radius=20)

        # text
        self.text = font.render(text, True, text_color)
        self.text_rect = self.text.get_rect(center=(width // 2, height // 2))
        self.image.blit(self.text, self.text_rect)

        self.rect = self.image.get_rect(center=pos)

        self.action = action

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed[0]:
                self.action()