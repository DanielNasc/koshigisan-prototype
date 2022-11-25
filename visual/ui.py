import pygame
from settings import *
from game_stats_settings import gameStats
from support.sprites_support import import_a_single_sprite

class UI:
    def __init__(self):
        
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)
        self.font_bar = pygame.font.Font(UI_FONT,UI_BAR_FONT_SIZE)
        self.font_controls = pygame.font.Font(UI_FONT,UI_CONTROLS_FONT_SIZE)
        self.is_controls_open = False

        # icons
        self.heart = "assets/sprites/ui/heart.png"
        self.mana = "assets/sprites/ui/mana.png"

        # texts
        self.hp_text = "HP"
        self.mana_text = "MANA"

        # setup bar
        self.health_bar_rect = pygame.Rect(70,20,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.mana_bar_rect = pygame.Rect(130,69,MANA_BAR_WIDTH,BAR_HEIGHT)

        # convert weapon dictionary
        self.weapon_graphics = []
        for weapon in weapons_ui_data.values():
            weapon_path = weapon['graphic']
            weapon = pygame.image.load(weapon_path).convert_alpha()
            self.weapon_graphics.append(weapon)

        # convert magic dictionary
        self.magic_graphics = []
        for magic in magics_ui_data.values():
            magic_path = magic['graphic']
            magic = pygame.image.load(magic_path).convert_alpha()
            self.magic_graphics.append(magic)

        self.tab_time = 0
        self.tab_cooldown = 500

    def show_bar(self,current,max_amount,bg_rect,color,path,text):
        # draw bg
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        icon = import_a_single_sprite(path)

        # converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface,color,current_rect)
        border_rect = pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
        icon_rect = icon.get_rect(topright = (border_rect.topleft[0] - 10, border_rect.topleft[1] - 5))
        self.display_surface.blit(icon, icon_rect)

        # text
        text_surf = self.font_bar.render(text,False,TEXT_COLOR)
        text_rect = text_surf.get_rect(topleft = (border_rect.topright[0] + 10,border_rect.topright[1]))
        self.display_surface.blit(text_surf,text_rect)

    def bar_rect(self,x,y,width,height):
        bg_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR,bg_rect, border_radius = 7)
        return pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,bg_rect.inflate(12,12),3)

    def show_exp(self,exp):
        text_surf = self.font.render(str(int(exp)),False,TEXT_COLOR)
        x = self.display_surface.get_width() - 30
        y = self.display_surface.get_height() - 20
        text_rect = text_surf.get_rect(bottomright = (x,y))
        coin = import_a_single_sprite('assets/sprites/ui/coin.png', 2)

        pygame.draw.rect(self.display_surface, UI_BG_COLOR,text_rect.inflate(20,20))
        self.display_surface.blit(text_surf,text_rect)
        border_rect = pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,text_rect.inflate(20,20),3)
        coin_rect = coin.get_rect(topright = (border_rect.topleft[0] - 15, y - 33))
        self.display_surface.blit(coin, coin_rect)

    def selection_box(self,left,top, has_switched):
        bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        
        if has_switched:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR_ACTIVE,bg_rect,3)
        else:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
        return bg_rect

    def weapon_overlay(self,weapon_index,has_switched):
        bg_rect = self.selection_box(10,630,has_switched) # weapon
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(weapon_surf,weapon_rect)

    def magic_overlay(self,magic_index,has_switched):
        bg_rect = self.selection_box(80,635,has_switched) # magic
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(magic_surf,magic_rect)

    def set_text(self,text,x,y,color):
        # text
        text_surf = self.font_controls.render(text,False,color)
        text_rect = text_surf.get_rect(topleft = (x,y))
        self.display_surface.blit(text_surf,text_rect)
    
    def controls_text(self):
        self.set_text("Mover:", 20, 168, HEALTH_COLOR)
        self.set_text("[↑, →, ↓, ←]", 20, 188, TEXT_COLOR)
        self.set_text("Atacar:", 20, 208, HEALTH_COLOR)
        self.set_text("[X]", 90, 208, TEXT_COLOR)
        self.set_text("Usar Magia:",20, 228, HEALTH_COLOR)
        self.set_text("[Z]",120, 228, TEXT_COLOR)
        self.set_text("Interagir:", 20, 248, HEALTH_COLOR)
        self.set_text("[SHIFT ESQUERDO]", 20, 268, TEXT_COLOR)
        self.set_text("Abrir/Fechar o", 20, 288, HEALTH_COLOR)
        self.set_text("Menu Upgrade:", 20, 308, HEALTH_COLOR)
        self.set_text("[M]", 140, 308, TEXT_COLOR)
        self.set_text("Comprar Upgrade:", 20, 328, HEALTH_COLOR)
        self.set_text("[ESPAÇO]", 20, 348, TEXT_COLOR)

    def controls(self):
        self.bar_rect(10, 148, CONTROLS_RECT_WIDTH, CONTROLS_RECT_HEIGHT)
        self.controls_text()

    def controls_title(self):
        rect = self.bar_rect(10, 148, CONTROLS_RECT_WIDTH, TITLE_CONTROLS_HEIGHT)
        text_surf = self.font_bar.render("CONTROLES [TAB]",False,TEXT_COLOR)
        text_rect = text_surf.get_rect(center = rect.center)
        self.display_surface.blit(text_surf,text_rect)
    
    def change_controls(self):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_TAB] and (pygame.time.get_ticks() - self.tab_time >= self.tab_cooldown)):
            self.is_controls_open = not self.is_controls_open
            self.tab_time = pygame.time.get_ticks()
        # for event in pygame.event.get():
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_TAB:
    
    def show_enemies(self,enemies):
        text_surf = self.font.render(str(int(enemies)),False,TEXT_COLOR)
        x = self.display_surface.get_width() - 20
        y = 20
        text_rect = text_surf.get_rect(topright = (x,y))
        enemy = import_a_single_sprite('assets/sprites/ui/enemy.png', 2)

        pygame.draw.rect(self.display_surface, UI_BG_COLOR,text_rect.inflate(20,20))
        self.display_surface.blit(text_surf,text_rect)
        border_rect = pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,text_rect.inflate(20,20),3)
        enemy_rect = enemy.get_rect(topright = (border_rect.topleft[0] - 10, border_rect.centery - 20))
        self.display_surface.blit(enemy, enemy_rect)

    def update_text(self, player):
        self.hp_info = f'{round(gameStats.player_health, 1)}/{round(gameStats.player_stats["health"], 1)}'
        self.mana_info = f'{round(player.mana, 1)}/{round(player.stats["mana"], 1)}'

    def display(self,player):
        self.bar_rect(10, 10, BAR_RECT_WIDTH, BAR_RECT_HEIGHT)
        self.update_text(player)
        self.set_text(self.hp_info, 162, 46, TEXT_COLOR)
        self.set_text(self.mana_info, 216, 92, TEXT_COLOR)
        self.show_bar(gameStats.player_health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR,self.heart,self.hp_text)
        self.show_bar(player.mana,player.stats['mana'],self.mana_bar_rect,MANA_COLOR,self.mana,self.mana_text)
        
        self.show_exp(gameStats.player_exp)
        self.show_enemies(gameStats.enemies_amount) 
        self.change_controls()

        if(self.is_controls_open): 
            self.controls()
        else:
            self.controls_title()
        
        self.weapon_overlay(player.weapon_index, player.is_attacking)
        self.magic_overlay(player.magic_index, player.is_attacking_w_magic)



