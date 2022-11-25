import pygame
from support.sprites_support import import_animations_from_folder
from random import choice

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self,pos,animation_frames,groups, anim_speed=None):
        super().__init__(groups)
        self.sprite_type = "magic"
        self.frame_index = 0
        self.animation_speed = 0.25 if not anim_speed else anim_speed
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
            'flame': import_animations_from_folder('assets/FX/particles/flame'),
            'continuous': import_animations_from_folder('assets/FX/particles/continuous', 1),
            'snow': import_animations_from_folder('assets/FX/particles/snow'),
            'thunder': import_animations_from_folder('assets/FX/particles/thunder'),
            'fire': import_animations_from_folder('assets/FX/particles/fire'),

            # monsters deaths
            'nukekubi': import_animations_from_folder('assets/FX/particles/smoke', 0.5),
            'eagle': import_animations_from_folder('assets/FX/particles/smoke_orange', 0.25),
            'snow_skeleton': import_animations_from_folder('assets/FX/particles/smoke', 0.5),
            'thunder_skeleton': import_animations_from_folder('assets/FX/particles/smoke_orange', 0.5),
            'fire_skeleton': import_animations_from_folder('assets/FX/particles/smoke_orange', 0.5),
            'akuma': import_animations_from_folder('assets/FX/particles/smoke', 2),

            # leafs
            'leafs': (
                import_animations_from_folder('assets/FX/particles/leafs/leaf1'),
                import_animations_from_folder('assets/FX/particles/leafs/leaf2'),
                import_animations_from_folder('assets/FX/particles/leafs/leaf3'),
                import_animations_from_folder('assets/FX/particles/leafs/leaf4'),
                import_animations_from_folder('assets/FX/particles/leafs/leaf5'),
                import_animations_from_folder('assets/FX/particles/leafs/leaf6'),
                self.invert(import_animations_from_folder('assets/FX/particles/leafs/leaf1')),
                self.invert(import_animations_from_folder('assets/FX/particles/leafs/leaf2')),
                self.invert(import_animations_from_folder('assets/FX/particles/leafs/leaf3')),
                self.invert(import_animations_from_folder('assets/FX/particles/leafs/leaf4')),
                self.invert(import_animations_from_folder('assets/FX/particles/leafs/leaf5')),
                self.invert(import_animations_from_folder('assets/FX/particles/leafs/leaf6')),
            ),

            'bamboo': (
                import_animations_from_folder('assets/FX/particles/bamboos/bamboo1'),
                self.invert(import_animations_from_folder('assets/FX/particles/bamboos/bamboo1')),
                import_animations_from_folder('assets/FX/particles/bamboos/bamboo2'),
                self.invert(import_animations_from_folder('assets/FX/particles/bamboos/bamboo2')),
                import_animations_from_folder('assets/FX/particles/bamboos/bamboo3'),
                self.invert(import_animations_from_folder('assets/FX/particles/bamboos/bamboo3')),
                import_animations_from_folder('assets/FX/particles/bamboos/bamboo4'),
                self.invert(import_animations_from_folder('assets/FX/particles/bamboos/bamboo4'))
            ),

            'rocks': (
                import_animations_from_folder('assets/FX/particles/rocks/rocks1'),
                self.invert(import_animations_from_folder('assets/FX/particles/rocks/rocks1')),
                import_animations_from_folder('assets/FX/particles/rocks/rocks2'),
                self.invert(import_animations_from_folder('assets/FX/particles/rocks/rocks2')),
                import_animations_from_folder('assets/FX/particles/rocks/rocks3'),
                self.invert(import_animations_from_folder('assets/FX/particles/rocks/rocks3')),
                import_animations_from_folder('assets/FX/particles/rocks/rocks4'),
                self.invert(import_animations_from_folder('assets/FX/particles/rocks/rocks4'))
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
    
    def create_leafs_particles(self,pos,groups):
        animation_frames = choice(self.frames['leafs'])
        ParticleEffect(pos,animation_frames,groups)

    def create_rocks_particles(self,pos,groups):
        animation_frames = choice(self.frames['rocks'])
        ParticleEffect(pos,animation_frames,groups)

    def create_particles(self,animation_type,pos,groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos,animation_frames,groups)
