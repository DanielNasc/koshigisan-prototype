import pygame

from settings import *
from level import *
from assets.cutscenes.intro.intro import IntroCutscene
from assets.cutscenes.game_over.gameover import GameOverCutscene
from assets.cutscenes.victory.victory import VictoryCutscene
from menu import *

class Game:
    def __init__(self) -> None:
        pygame.init() # Initialize all imported pygame modules.
        pygame.display.set_caption("Koshigisan") #This function will change the name on the window

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # This function will create a display Surface
        self.clock = pygame.time.Clock()

        self.is_in_transition = False
        self.to = None
        self.black_screen = pygame.surface.Surface((WIDTH, HEIGHT))
        self.black_screen.fill((0, 0, 0, 0))
        self.black_screen_rect = self.black_screen.get_rect(topleft = (0, 0))
        self.black_screen_opacity = 0
        self.black_screen_opacity_speed = 3

        self.levels = ["Intro", "Menu","Sky", "Hell", "Game Over", "Win"]
        self.level_index = 0
        self.create_level()

        self.upgrade_menu_time = 0

    def create_level(self):
        if (self.level_index == 0):
            self.level = IntroCutscene()
            gameStats.reset_player_stats()
            
        elif self.level_index == 1:
            self.level = Menu(self.update_level)
            gameStats.reset_player_stats()

        elif self.level_index == 2:
            pygame.mixer.music.load("assets/SFX/tankoubusi.WAV")
            pygame.mixer.music.set_volume(0.8)
            self.level = Level(self.levels[self.level_index], self.level_transition, self.level_index - 1) # create a instance of Level class
            pygame.mixer.music.play(loops=-1)

        elif self.level_index == 3:
            pygame.mixer.music.load("assets/songs/songs_level_4/1º_Ato_L4.mp3")
            self.level = Level(self.levels[self.level_index], self.win, self.level_index - 1) # create a instance of Level class
            pygame.mixer.music.play(loops=-1)

        elif self.level_index == 4:
            self.level = GameOverCutscene()
        else:
            self.level = VictoryCutscene()

    def win(self):
        self.level_transition(5)

    def level_transition(self, to: int = None):
        if self.is_in_transition:
            self.black_screen.set_alpha(self.black_screen_opacity)
            self.screen.blit(self.black_screen, self.black_screen_rect)
            self.black_screen_opacity += self.black_screen_opacity_speed
            if (self.black_screen_opacity > 255):
                self.is_in_transition = False
                self.update_level(self.to)
                self.to = None
                self.black_screen_opacity = 0
        else:
            self.to = to
            self.is_in_transition = True


    def update_level(self, to: int =None):
        del self.level

        if (to != None):
            self.level_index = to
        else:
            self.level_index += 1

        if (self.level_index >= len(self.levels)):
            self.level_index = 0

        pygame.mixer.stop()
        pygame.mixer.music.unload()
        
        self.create_level()

    def run(self):
        while True:
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_m]):
                if (hasattr(self.level, "toggle_menu") and (pygame.time.get_ticks() - self.upgrade_menu_time >= 500)):
                            self.level.toggle_menu()
                            self.upgrade_menu_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                        

            self.screen.fill('black') # Fill the Surface with a solid color.
            self.level.run()

            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[pygame.K_j]:
                self.update_level()

            if (hasattr(self.level, "ended")):
                if self.level.ended:
                    self.level_transition(1)

            # gambiarra temporária
            if (hasattr(self.level, 'player')):
                p_topleft = self.level.player.rect.topleft

                # if (p_topleft[0] >= 640 and p_topleft[0] <= 768) and p_topleft[1] >= 2050 and self.level_index == 2:
                #     self.update_level()

                if (self.level.player.is_dead):
                    self.level_transition(4)

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()