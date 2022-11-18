import time

from level import CutsceneController
from anim_enitity import AnimEntity

from assets.cutscenes.victory.v_settings import STAGES

class VictoryCutscene(CutsceneController):
    def __init__(self) -> None:
        super().__init__()

        # self.sounds = {
        #     "main": pygame.mixer.Sound("assets/sounds/Intro/sss.mp3")
        # }

        # self.sounds["main"].play()

        for name, data in STAGES["init"]["entities"].items():
            AnimEntity(name, data, self.visible_sprites, .1)

        self.initialization_time = time.time()
        self.major_events = STAGES["events"].copy()

        self.ended = False
