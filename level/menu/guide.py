import pygame
from settings import *
from level.menu.button import Button

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
                "#942C4B",
                self.font, 
                "white",
                (self.close_button, self.visible_sprites),
                20,  (148, 44, 75, 128), "#C7424F",
                self.close)


    def get_text(self):
        self.create_text("INSTRUÇÔES:", 0)
        self.create_act_desc_text("Mover >>", " ↑, →, ↓, ←",2)
        self.create_act_desc_text("Atacar >>", " X",3) 
        self.create_act_desc_text("Usar Magia (Consome Mana) >>", " Z",4)
        self.create_act_desc_text("Interagir >>", " SHIFT",5)
        self.create_act_desc_text("Abrir/Sair Menu de Upgrade (Consome Moedas) >>", " M",6)
        self.create_act_desc_text("Aprimorar habilidade >> ", "ESPAÇO",7)
        self.create_text("0 HP = GAME OVER. Mate todos os inimigos para vencer!",8)

    def create_act_desc_text(self, action, desc, text_pos):
        act = self.font.render(action, True, '#C7424F')
        desc = self.font.render(desc, True, 'white')

        act_rect =  act.get_rect(topleft=(self.width // 15, 20 + self.height // 13 * text_pos))
        desc_rect = self.text.get_rect(topleft=((self.width // 15) + act_rect.width, 20 + self.height // 13 * text_pos))

        self.image.blit(act,act_rect)
        self.image.blit(desc, desc_rect)

    def create_text(self, text, text_pos):
        self.text = self.font.render(text, True, 'white')
        self.text_rect = self.text.get_rect(topleft=(self.width // 15, 20 + self.height // 13 * text_pos))
        self.image.blit(self.text, self.text_rect)

    def close(self):
        for button in self.close_button:
            button.kill()
        self.kill()
        self.restore_buttons()

    def update(self):
        self.visible_sprites.update()

        # if self.rect.collidepoint(mouse_pos):
        #     if mouse_pressed[0]:
        #         self.kill()