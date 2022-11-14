import pygame
from datetime import datetime as dt

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
        
        self.anim = import_sprites(data["path"], 3)
        self.anim_type = data["anim_type"]
        self.from_pos = data["from"]
        self.to = data["to"]
        self.animation_after_stopped = data["animation_after_stopped"]
        self.events = data["events"]

        self.is_in_event = False
        self.spawn_time = dt.now().second

        self.status = "down_idle"
        self.image = self.anim[self.status][self.frame_index]
        self.sprite_dir = "down"

        self.rect = self.hitbox = self.image.get_rect(center = self.from_pos)

        self.direction = pygame.math.Vector2(
            (
                self.to[0] - self.from_pos[0],
                self.to[1] - self.from_pos[1]
            )
        )


        # if self.direction.magnitude() != 0:
        #     self.direction = self.direction.normalize()

    def get_sprite_direction(self):
        self.sprite_dir = "down"

        if self.direction.y != 0:
            self.sprite_dir = "down" if self.direction.y < 0 else "up"

        if self.direction.x != 0:
            self.sprite_dir = "left" if self.direction.x < 0 else "right"


    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not self.animation_after_stopped in self.status:
                self.status = self.animation_after_stopped
                self.frame_index = 0
        else:
            if not "move" in self.status:
                self.status = self.sprite_dir + "_move"
                self.frame_index = 0

    def event_manager(self):
        curr_tick = dt.now().second

        for event in self.events:
            if event["time"] + self.spawn_time <= curr_tick:
                self.is_in_event = True
                self.status = event["animation"]


    def animate(self):
        animation = self.anim[self.status]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[floor(self.frame_index)]
        self.rect = self.image.get_rect(center = self.rect.center)

    def detect_collision(self, _):
        return 

    def movement_controller(self):
        self.direction.x = 0 if abs(self.to[0]) <= abs(self.rect.center[0]) else self.direction.x
        self.direction.y = 0 if abs(self.to[1]) <= abs(self.rect.center[1]) else self.direction.y

    def update(self) -> None:
        self.event_manager()
        self.movement_controller()
        if not self.is_in_event:
            self.get_sprite_direction()
            self.get_status()
        self.animate()
        self.move(1)