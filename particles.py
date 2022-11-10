import pygame
from support import import_animations_from_folder
from spritesheet import SpriteSheet
from random import choice

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self,pos,animation_frames,groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
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
            #leafs
            'leaf': (
                SpriteSheet('assets/FX/particles/Leaf.png').get_all(12,7),
                SpriteSheet('assets/FX/particles/Grass.png').get_all(12,13),
                self.invert(SpriteSheet('assets/FX/particles/Leaf.png').get_all(12,7)),
                self.invert(SpriteSheet('assets/FX/particles/Grass.png').get_all(12,13)),
            ),

            'bamboo': SpriteSheet('assets/FX/particles/Bamboo.png').get_all(16,15)

        }
    
    def invert(self,frames):
        new_frames = []

        for frame in frames:
            flipped_frame = pygame.transform.flip(frame,True,False)
            new_frames.append(flipped_frame)
        
        return new_frames

    def create_bamboo_particles(self,pos,groups):
        animation_frames = self.frames['bamboo']
        ParticleEffect(pos,animation_frames,groups)