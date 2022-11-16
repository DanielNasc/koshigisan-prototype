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
        self.clicked = False
        pos = (
            pos[0] - (width // 2),
            pos[1] - (height // 2)
        )
        self.top_rect = pygame.Rect(pos,(width,height))
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.top_color = color
        self.bottom_color = shadow

        self.screen = pygame.display.get_surface()

    def update(self):
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        
        top_rect = self.top_rect.copy()
        bottom_rect = self.bottom_rect.copy()
        bottom_rect.x += 10
        bottom_rect.y += 10
        text_rect = self.text_rect.copy()
        if top_rect.collidepoint(mouse_pos):
            self.top_color = self.color
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
                bottom_rect.inflate_ip(self.elevation, self.elevation)
                top_rect.inflate_ip(self.elevation, self.elevation)
                text_rect.center = (
                    text_rect.centerx + (self.elevation // 2),
                    text_rect.centery + (self.elevation // 2)
                )

            elif pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
            self.top_color = self.hover
        else:
            self.top_color = self.color

        bottom_surf = pygame.Surface(bottom_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(bottom_surf, self.bottom_color, (0, 0, *bottom_rect.size), border_radius = 12)
        self.screen.blit(bottom_surf, bottom_rect.topleft)

        top_surf = pygame.Surface(top_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(top_surf, self.top_color, (0, 0, *top_rect.size), border_radius = 12)
        top_surf.blit(self.text, text_rect)
        self.screen.blit(top_surf, top_rect.topleft)

        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed[0]:
                self.action()