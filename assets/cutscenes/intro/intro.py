from level import CutsceneController
from  anim_enitity import AnimEntity

from assets.cutscenes.intro.i_settings import STAGES

class IntroCutscene(CutsceneController):
    def __init__(self) -> None:
        super().__init__()

        for name, data in STAGES["init"]["entities"].items():
            AnimEntity(name, data, self.visible_sprites)