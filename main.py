import pygame

from settings import *
from level.level import *
from cutscenes.intro.intro import IntroCutscene
from cutscenes.game_over.gameover import GameOverCutscene
from cutscenes.victory.victory import VictoryCutscene
from level.menu.menu import *

class Game:
    def __init__(self) -> None:
        pygame.init() # Initialize all imported pygame modules.
        pygame.display.set_caption("Koshigisan") #This function will change the name on the window

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # This function will create a display Surface
        self.clock = pygame.time.Clock()

        # Inicializa as variáveis para o efeito de transição entre telas (fade in/out)
        self.is_in_transition = False
        self.to = None
        self.black_screen = pygame.surface.Surface((WIDTH, HEIGHT))
        self.black_screen.fill((0, 0, 0, 0))
        self.black_screen_rect = self.black_screen.get_rect(topleft = (0, 0))
        self.black_screen_opacity = 0
        self.black_screen_opacity_speed = 3

        # Todas as telas do jogo são tratadas como níveis
        self.levels = ["Intro", "Menu","Sky", "Hell", "Game Over", "Win"]
        self.level_index = 0
        self.create_level()

        self.upgrade_menu_time = 0

    # Cria um nível de acordo com o índice atual
    def create_level(self):
        if (self.level_index == 0):
            self.level = IntroCutscene()
            gameStats.reset_player_stats()
            
        elif self.level_index == 1: # Menu
            self.level = Menu(self.update_level)
            gameStats.reset_player_stats() # Reseta os stats do player quando o jogador volta para o menu, para que não fique com os stats do último jogo

        elif self.level_index == 2: # Sky
            pygame.mixer.music.load("assets/SFX/tankoubusi.WAV") 
            pygame.mixer.music.set_volume(0.8)
            self.level = Level(self.levels[self.level_index], self.level_transition, self.level_index - 1) # create a instance of Level class
            pygame.mixer.music.play(loops=-1)

        elif self.level_index == 3: # Hell
            pygame.mixer.music.load("assets/songs/songs_level_4/1º_Ato_L4.mp3")
            self.level = Level(self.levels[self.level_index], self.win, self.level_index - 1) # create a instance of Level class
            pygame.mixer.music.play(loops=-1)

        elif self.level_index == 4: # Game Over
            self.level = GameOverCutscene()
        else: # Win
            self.level = VictoryCutscene()

    def win(self):
        self.level_transition(5) # vai para o indice 5 do array de levels, que é a tela de vitória

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
        # Destroi o level atual e cria um novo
        del self.level

        # Se o proximo level não for especificado, vai para o proximo direto
        if (to != None):
            self.level_index = to
        else:
            self.level_index += 1

        # Se o proximo level for maior que o numero de levels, volta para o primeiro
        if (self.level_index >= len(self.levels)):
            self.level_index = 0

        # Para de tocar a musica do level anterior
        pygame.mixer.stop()
        pygame.mixer.music.unload()
        
        # Cria o novo level
        self.create_level()

    def run(self):
        # Loop principal do jogo
        while True:
            self.clock.tick(FPS) # This function will limit the while loop to a max of 60 times per second.s
            pressed_keys = pygame.key.get_pressed()
            
            # Abre o menu de upgrades se a tecla M for pressionada
            if (pressed_keys[pygame.K_m]):
                if (hasattr(self.level, "toggle_menu") and (pygame.time.get_ticks() - self.upgrade_menu_time >= 500)):
                            self.level.toggle_menu()
                            self.upgrade_menu_time = pygame.time.get_ticks()

            # Fecha o jogo se o X da janela for pressionado
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                        

            self.screen.fill('black') # Fill the Surface with a solid color.
            self.level.run() # Run the level

            if pressed_keys[pygame.K_j]: # Tecla Cheat para pular de level
                self.update_level()

            if (hasattr(self.level, "ended")): # Quando a animação de fim de jogo terminar, volta para o menu
                if self.level.ended:
                    self.level_transition(1)

            if (hasattr(self.level, 'player')): # Se o player morrer, vai para a tela de game over
                if (self.level.player.is_dead):
                    self.level_transition(4)

            pygame.display.update() # This function will update the contents of the entire display.

if __name__ == "__main__":
    game = Game()
    game.run()