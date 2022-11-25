import pygame
from time import time

from support.sprites_support import import_animations_from_folder
from entities.anim_enitity import AnimEntity
from visual.particles import *

class CutsceneController():
    def __init__(self) -> None:
        self.visible_sprites = pygame.sprite.Group()
        self.display_suface = pygame.display.get_surface()
        self.major_events = []
        self.sounds = {}
        self.texts = {}

    def convert_pos(self, pos, offset):
        if pos == "screen_center":
            return (
                (self.display_suface.get_width() // 2) - offset[0],
                (self.display_suface.get_height() // 2) - offset[1]
            )

    def major_events_manager(self):
        curr_tick = time()
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
        self.display_suface.fill((0, 0, 0))
        self.major_events_manager()
        self.visible_sprites.draw(self.display_suface)
        self.visible_sprites.update()


