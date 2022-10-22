import pygame
import sys
from settings import *

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Koshigisan")


    def run(self):
        font = pygame.font.SysFont(None, 24)
        img = font.render("Hello, Koshigisan!", True, "white")

        img_pos_x = (WIDTH // 2) - (img.get_width() // 2)
        img_pos_y = (HEIGHT // 2) - (img.get_height() // 2)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('black')
            self.screen.blit(img, (img_pos_x, img_pos_y))

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()