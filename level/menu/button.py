import pygame
from game_stats_settings import *

class Button(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, text, color, font, text_color, groups, elevation, shadow, hover, action=None):
        super().__init__(groups)

        # button with rounded corners
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))

        # pygame.draw.rect(self.image, color, (0, 0, width, height), border_radius=20)

        # text
        self.text = font.render(text, True, text_color)
        self.text_rect = self.text.get_rect(center=(width // 2, height // 2))

        self.rect = self.image.get_rect(center=pos)

        self.action = action

        self.elevation = elevation
        self.original_y_pos = pos[1]
        self.color = color
        self.color_shadow = shadow
        self.hover = hover
        pos = (
            pos[0] - (width // 2),
            pos[1] - (height // 2)
        )
        self.top_rect = pygame.Rect(pos,(width,height))
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.top_color = color
        self.bottom_color = shadow

        self.screen = pygame.display.get_surface()

        self.press_time = 0

    def handle_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        curr_time = time.time()

        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.hover

            if pygame.mouse.get_pressed()[0] and (curr_time - self.press_time >= 500):
                self.press_time = curr_time
                self.action()
            
        else:
            self.top_color = self.color
    
    def update(self):
        self.handle_mouse()

        top_rect = self.top_rect.copy()

        bottom_rect = self.bottom_rect.copy()
        bottom_rect.x += 10
        bottom_rect.y += 10
        text_rect = self.text_rect.copy()

        # desenha a sombra do botão
        bottom_surf = pygame.Surface(bottom_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(bottom_surf, self.bottom_color, (0, 0, *bottom_rect.size), border_radius = 12)
        self.screen.blit(bottom_surf, bottom_rect.topleft)

        # desenha o botão em si
        top_surf = pygame.Surface(top_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(top_surf, self.top_color, (0, 0, *top_rect.size), border_radius = 12)
        top_surf.blit(self.text, text_rect)

        self.screen.blit(top_surf, top_rect.topleft)