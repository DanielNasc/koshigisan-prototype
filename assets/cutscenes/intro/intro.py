import pygame, time

from level import CutsceneController
from particles import ParticleEffect
from support import import_animations_from_folder
from anim_enitity import AnimEntity

from assets.cutscenes.intro.i_settings import STAGES

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
        self.major_events = STAGES["events"]

        self.ended = False

    def major_events_manager(self):
        curr_tick = time.time()
        satisfied_events = []

        for index, event in enumerate(self.major_events):
            if event["time"] + self.initialization_time <= curr_tick:
                if event["type"] == "invoke_particle":
                    particle_animation = import_animations_from_folder(f'assets/FX/particles/{event["particle"]}', event["scale"])
                    initial_pos = event["from"]
                    direction = event["direction"]
                    particle_w = particle_animation[0].get_width() 
                    particle_h = particle_animation[0].get_height()

                    for i in range(event["amount"]):
                        pos = (
                            initial_pos[0] +  (i * particle_w * event["spacing"] * direction[0]),
                            initial_pos[1] +  (i * particle_h * event["spacing"] * direction[1])
                        )
                        ParticleEffect(pos, particle_animation, self.visible_sprites, .03)
                elif event["type"] == "stop_sound":
                    self.sounds[event["wich"]].stop()
                elif event["type"] == "init_sound":
                    self.sounds[event["name"]] = pygame.mixer.Sound(event["path"])
                    self.sounds[event["name"]].play()
                    # if event["name"] == "scream":
                    #     self.sounds[event["name"]].set_volume(1)
                elif event["type"] == "invoke_entity":
                    AnimEntity(event["name"], event["data"], self.visible_sprites, .1)

                elif event["type"] == "end":
                    self.ended = True
                satisfied_events.append(index)

        satisfied_events.reverse()
        for index in satisfied_events:
            self.major_events.pop(index)

    def run(self):
        self.major_events_manager()
        super().run()
