import pygame
import sys
import time

class GameStats:
    def __init__(self):
        self.DIFFICULT = 1
        self.DIFFICULT_VALUES_VARIATION_PERCENTAGE = .5

        self.set_difficult_time = 0
        self.set_difficult_cooldown = .5

        self.player_stats = {
                        'health': self.calculate_property_by_difficult(100), 
                        'mana': 60, 
                        'attack': self.calculate_property_by_difficult(10), 
                        'speed': 2, 
                        'magic': self.calculate_property_by_difficult(4)
                    }
        self.player_stats_backup = self.player_stats.copy()
        self.player_exp = 100
        self.player_health = self.player_stats["health"]
        self.player_mana = self.player_stats['mana']
        
        self.enemies_amount = 0

        self.is_fullscreen = False
        self.toggle_fullscreen_time = 0

    def reset_player_stats(self):
        self.player_stats = self.player_stats_backup.copy()
        self.player_exp = 100
        self.player_health = self.player_stats["health"]

    def calculate_property_by_difficult(self, prop, invert_sign=False):
        return prop + ( prop * self.DIFFICULT_VALUES_VARIATION_PERCENTAGE * self.DIFFICULT * (-1 if invert_sign else 1) )

    def set_difficult(self):
        if time.time() - self.set_difficult_time > self.set_difficult_cooldown:
            self.DIFFICULT += 1
            if self.DIFFICULT > 1:
                self.DIFFICULT = -1
            self.set_difficult_time = time.time()
    
    def close(self):
        pygame.quit()
        sys.exit()

    def get_difficult(self):
        return self.DIFFICULT
    
    def change_screen(self):
        curr_time = pygame.time.get_ticks()

        if curr_time -self.toggle_fullscreen_time >= 500:
            pygame.display.toggle_fullscreen()
            self.is_fullscreen = not self.is_fullscreen
            self.toggle_fullscreen_time = curr_time

gameStats = GameStats()