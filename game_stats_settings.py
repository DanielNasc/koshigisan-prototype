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
        self.player_exp = 5000

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

gameStats = GameStats()