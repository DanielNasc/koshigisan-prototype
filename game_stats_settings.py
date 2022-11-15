import pygame
import time

class GameStats:
    def __init__(self):
        self.DIFFICULT = 1
        self.DIFFICULT_VALUES_VARIATION_PERCENTAGE = .5

        self.set_difficult_time = 0
        self.set_difficult_cooldown = 1

    def set_difficult(self):
        if time.time() - self.set_difficult_time > self.set_difficult_cooldown:
            self.DIFFICULT += 1
            if self.DIFFICULT > 1:
                self.DIFFICULT = -1
            self.set_difficult_time = time.time()

    def get_difficult(self):
        return self.DIFFICULT

gameStats = GameStats()