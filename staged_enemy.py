import pygame

from enemy import Enemy

"""
Estagios: [0] Idle, [1] Notar, [2] Preparar, [3] Atacar

[0] Idle: fica parado, esperando o player entrar em seu notice_radius
[1] Notar: Se movimenta quando o player entra em seu notice_radius
[2] Preparar: Fica estático por pouco tempo, dando a ideia de estar se preparando e dando tempo do player se esquivar
[3] Atacar: Efetua o ataque

"""

IDLE = 0
NOTICE = 1
PREPARE = 2
ATTACK = 3

class StagedEnemy(Enemy):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, slippery_sprites) -> None:
        super().__init__(monster_name, pos, groups, obstacle_sprites, slippery_sprites)
        self.stage = 0
        self.prepare_time = 200
        self.preprae_tick = None
        self.attack_duration = 2000

    def prepare(self):
        curr_tick = pygame.time.get_ticks()

        if (self.status == PREPARE):
            if (curr_tick - self.preprae_tick >= self.prepare_time):
                self.stage = ATTACK
                self.is_blocked = False
        elif (self.status == NOTICE):
            self.is_blocked = True

    def attack(self):
        curr_tick = pygame.time.get_ticks()

        # Se o tempo de ataque ja tiver acabado, ele sai do stage de ataque
        if (self.is_attacking and curr_tick - self.attack_time >= self.attack_duration):
            self.is_attacking = False
            self.stage = 0
            return

        self.attack_time = curr_tick
        self.is_attacking = True

        if self.attack_type == "dash":
            self.speed_boost = 2
        else:
            self.speed_boost = 1
        
    def update_stage(self, player):
        distance = self.get_player_distance_and_direction(player)[0]

        if (distance <= self.attack_radius):
            if (self.stage < ATTACK):
                self.prepare()
        elif (distance <= self.notice_radius):
            self.stage = NOTICE
        else:
            self.stage = IDLE

    def update(self):
        return super().update()

    def enemy_update(self, player):
        self.update_stage()
        return super().enemy_update(player)