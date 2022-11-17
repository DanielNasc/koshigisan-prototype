import pygame, time

from math import floor

from entity import Entity
from support import import_sprites


"""
    "anim_type": "move",
    "from": (x, y),
    "to": (u, v)
"""

class AnimEntity(Entity):
    def __init__(self, name, data, groups, anim_speed = .15) -> None:
        super().__init__(groups)
        self.name = name
        
        self.scale = data["scale"]
        self.anim = import_sprites(data["path"], self.scale)
        self.anim_type = data["anim_type"]
        self.from_pos = data["from"]
        self.to = data["to"]
        self.animation_after_stopped = data["animation_after_stopped"]
        self.events = data["events"].copy()
        self.animation_speed = anim_speed

        self.is_in_event = False
        self.spawn_time = time.time()

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

        self.stopped = False


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
            if self.name == "Yamato":
                self.status = self.sprite_dir
            elif not "move" in self.status:
                self.status = self.sprite_dir + "_move"
                self.frame_index = 0

    def check_requirements(self, requirements):
        for requirement in requirements:
            if requirement == "stopped":
                if not (self.direction.x == 0 and self.direction.y == 0):
                    return False
            if requirement == "animation_after_stopped":
                if not (self.status == self.animation_after_stopped):
                    return False
        return True

    def event_manager(self):
        curr_tick = time.time()
        satisfied_events = []

        for index, event in enumerate(self.events):
            if "time" in event:
                if event["time"] + self.spawn_time <= curr_tick:
                    self.is_in_event = True
                    if event["type"] == "dance":
                        self.status = event["animation"]
                    elif event["type"] == "die":
                        self.kill()
                    satisfied_events.append(index)
            elif self.check_requirements(event["required"]):
                if event["type"] == "rescale":
                    self.is_in_event = True
                    
                    for anim_array  in self.anim.values():
                        for i in range(len(anim_array)):
                            player_size_vector = pygame.math.Vector2(anim_array[i].get_size())
                            anim_array[i] = pygame.transform.scale(anim_array[i], player_size_vector * event["new_scale"])
                elif event["type"] == "init_sound":
                    pygame.mixer.Sound(event["path"]).play()

                satisfied_events.append(index)

        satisfied_events.reverse()
        for index in satisfied_events:
            self.events.pop(index)


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
        if not self.is_in_event:
            self.get_sprite_direction()
            self.get_status()
        self.event_manager()
        self.movement_controller()
        self.animate()
        self.move(1)
        self.event_manager()