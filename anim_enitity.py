import pygame

from math import floor

from entity import Entity
from support import import_sprites


"""
    "anim_type": "move",
    "from": (x, y),
    "to": (u, v)
"""

class AnimEntity(Entity):
    def __init__(self, name, data, groups) -> None:
        super().__init__(groups)
        self.name = name
        
        self.anim = import_sprites(data["path"], 2)
        self.anim_type = data["anim_type"]
        self.from_pos = data["from"]
        self.to = data["to"]

        self.status = "down_idle"
        self.image = self.anim[self.status][self.frame_index]

        self.rect = self.hitbox = self.image.get_rect(center = self.from_pos)

        self.direction = pygame.math.Vector2(
            (
                self.to[0] - self.from_pos[0],
                self.to[1] - self.from_pos[1]
            )
        )

        # if self.direction.magnitude() != 0:
        #     self.direction = self.direction.normalize()

    def animate(self):
        animation = self.anim[self.status]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[floor(self.frame_index)]
        self.rect = self.image.get_rect(center = self.rect.center)

    def detect_collision(self, direction):
        return 

    def movement_controller(self):
        self.direction.x = 0 if abs(self.to[0]) <= abs(self.rect.center[0]) else self.direction.x
        self.direction.y = 0 if abs(self.to[1]) <= abs(self.rect.center[1]) else self.direction.y

    def update(self) -> None:
        self.animate()
        self.movement_controller()
        self.move(2)