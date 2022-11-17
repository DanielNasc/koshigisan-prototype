import pygame
from settings import *
from game_stats_settings import gameStats
from support import import_a_single_sprite

class UI:
    def __init__(self):
        
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)
        self.font_bar = pygame.font.Font(UI_FONT,UI_BAR_FONT_SIZE)

        # icons
        self.heart = "assets/sprites/ui/heart.png"
        self.mana = "assets/sprites/ui/mana.png"
        self.hp_text = "HP"
        self.mana_text = "MANA"

        # setup bar
        self.health_bar_rect = pygame.Rect(70,20,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.mana_bar_rect = pygame.Rect(130,49,MANA_BAR_WIDTH,BAR_HEIGHT)

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

    def bar_rect(self):
        bg_rect = pygame.Rect(10,10,BAR_RECT_WIDTH,BAR_RECT_HEIGHT)
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect,border_radius = 7)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,bg_rect.inflate(12,12),3)

    def show_exp(self,exp):
        text_surf = self.font.render(str(int(exp)),False,TEXT_COLOR)
        x = self.display_surface.get_width() - 30
        y = self.display_surface.get_height() - 0
        text_rect = text_surf.get_rect(bottomright = (x,y))
        coin = import_a_single_sprite('assets/sprites/ui/coin.png', 1.5)

        pygame.draw.rect(self.display_surface, UI_BG_COLOR,text_rect.inflate(20,20))
        self.display_surface.blit(text_surf,text_rect)
        border_rect = pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,text_rect.inflate(20,20),3)
        coin_rect = coin.get_rect(topright = (border_rect.topleft[0] - 10, y - 25))
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

    def update_text(self, player):
        self.hp_text = f'{round(gameStats.player_health, 1)}/{round(gameStats.player_stats["health"], 1)} HP'
        self.mana_text = f'{round(player.mana, 1)}/{round(player.stats["mana"], 1)} MANA'

    def display(self,player):
        self.update_text(player)
        self.bar_rect()
        self.show_bar(gameStats.player_health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR,self.heart,self.hp_text)
        self.show_bar(player.mana,player.stats['mana'],self.mana_bar_rect,MANA_COLOR,self.mana,self.mana_text)
        self.show_exp(gameStats.player_exp) 
        
        self.weapon_overlay(player.weapon_index, player.is_attacking)
        self.magic_overlay(player.magic_index, player.is_attacking_w_magic)



