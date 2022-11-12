import pygame
from support import import_animations_from_folder
from spritesheet import SpriteSheet
from random import choice

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self,pos,animation_frames,groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.20
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()

class AnimationController:
    def __init__(self):
        self.frames = {
            # attacks
            'dash': import_animations_from_folder('assets/FX/particles/slash', 0.5),
            'continuous': import_animations_from_folder('assets/FX/particles/continuous', 0.5),

            # monsters deaths
            'nukekubi': import_animations_from_folder('assets/FX/particles/smoke', 0.5),
            'eagle': import_animations_from_folder('assets/FX/particles/smoke', 0.5),
            'akuma': import_animations_from_folder('assets/FX/particles/smoke', 0.5),

            # leafs
            'bamboo': (
                import_animations_from_folder('assets/FX/particles/leaf1', 0.5),
                import_animations_from_folder('assets/FX/particles/leaf2', 0.5),
                import_animations_from_folder('assets/FX/particles/leaf3', 0.5),
                import_animations_from_folder('assets/FX/particles/leaf4', 0.5),
                import_animations_from_folder('assets/FX/particles/leaf5', 0.5),
                import_animations_from_folder('assets/FX/particles/leaf6', 0.5),
                self.invert(import_animations_from_folder('assets/FX/particles/leaf1', 0.25)),
                self.invert(import_animations_from_folder('assets/FX/particles/leaf2', 0.25)),
                self.invert(import_animations_from_folder('assets/FX/particles/leaf3', 0.25)),
                self.invert(import_animations_from_folder('assets/FX/particles/leaf4', 0.25)),
                self.invert(import_animations_from_folder('assets/FX/particles/leaf5', 0.25)),
                self.invert(import_animations_from_folder('assets/FX/particles/leaf6', 0.25)),
            )

        }
    
    def invert(self,frames):
        new_frames = []

        for frame in frames:
            flipped_frame = pygame.transform.flip(frame,True,False)
            new_frames.append(flipped_frame)
        
        return new_frames

    def create_bamboo_particles(self,pos,groups):
        animation_frames = choice(self.frames['bamboo'])
        ParticleEffect(pos,animation_frames,groups)

    def create_particles(self,animation_type,pos,groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos,animation_frames,groups)
