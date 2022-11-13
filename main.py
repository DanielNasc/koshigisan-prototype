import pygame
import sys
from debug import debug

from settings import *
from level import Level

class Game:
    def __init__(self) -> None:
        pygame.init() # Initialize all imported pygame modules.
        pygame.display.set_caption("Koshigisan") #This function will change the name on the window

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # This function will create a display Surface
        self.clock = pygame.time.Clock()

        self.levels = ["Sky", "Hell"]
        self.level_index = 1
        self.level = Level(self.levels[self.level_index]) # create a instance of Level class

    def update_level(self):
        self.level_index += 1
        
        self.level = Level(self.levels[self.level_index])

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()

            self.screen.fill('black') # Fill the Surface with a solid color.
            self.level.run()

            p_topleft = self.level.player.rect.topleft

            # gambiarra temporária
            if (p_topleft[0] >= 640 and p_topleft[0] <= 768) and p_topleft[1] >= 2050 and self.level_index == 0:
                self.update_level()

            debug(self.level.player.health)
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()