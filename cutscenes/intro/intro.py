import pygame, time

from cutscenes.cutsceneController import CutsceneController
from entities.anim_enitity import AnimEntity

from cutscenes.intro.i_settings import STAGES

class IntroCutscene(CutsceneController):
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
