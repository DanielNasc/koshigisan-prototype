import pygame, time

from cutsceneController import CutsceneController
from entities.anim_enitity import AnimEntity

from cutscenes.game_over.gm_settings import STAGES

class GameOverCutscene(CutsceneController):
    def __init__(self) -> None:
        super().__init__()

        self.sounds = {
            "main": pygame.mixer.Sound("assets/sounds/Intro/sss.mp3")
        }

        self.sounds["main"].play()

        for name, data in STAGES["init"]["entities"].items():
            AnimEntity(name, data, self.visible_sprites)

        self.initialization_time = time.time()
        self.major_events = STAGES["events"].copy()

        self.ended = False

        self.font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 20)
        self.font_surf = self.font.render("GAME OVER", True, "White")
        self.font_rect = self.font_surf.get_rect(center = (self.display_suface.get_width() // 2, (self.display_suface.get_height() // 2) - 64 ))
    
    def run(self):
        super().run()
        self.display_suface.blit(self.font_surf, self.font_rect)
