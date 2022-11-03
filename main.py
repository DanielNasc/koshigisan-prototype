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

        self.level = Level() # create a instance of Level class


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black') # Fill the Surface with a solid color.
            self.level.run()

            debug((self.level.player.status, self.level.player.can_attack_w_magic, self.level.player.is_attacking_w_magic))
            pygame.display.update()
            self.clock.tick(FPS)
            

if __name__ == "__main__":
    game = Game()
    game.run()