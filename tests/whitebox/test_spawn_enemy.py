import pygame

import sys
import os
sys.path.append(os.path.dirname(__file__) + '/../..')

from level.level import Level
import level.level as level_module
from visual.camera import YSortCameraGroup

"""
    Testa se a classe Level está criando o inimigo corretamente, de acordo com o
    parâmetro passado.

    São 4 tipos de inimigos:
        - Aguia
        - Akuma
        - Esqueletos (3 tipos)
        - Nukekubi

    O fluxo da função spawn_enemy é o seguinte:
    1. Se o tipo estiver no array ["14", "A", "ske"]
        2. nome = ''
        3. Se o tipo for "A"
            4. nome = "akuma"
        5. Se o tipo for "14"
            6. nome = "eagle"
        7. Se o tipo for "ske"
            8. Se o level for "Sky"
                9. nome = "snow_skeleton"
            10. Se o level for "Hell"
                11. nome = choice(("snow_skeleton", "fire_skeleton", "thunder_skeleton"))
        12. Instancia um inimigo a partir da classe DashEnemy e baseado no nome
    13. Se não
        Cria-se uma Nukekubi a partir da classe ContinuousEnemy

"""

def test_spawn_akuma():
    pygame.init()
    pygame.display.set_mode((100, 100))

    # level_module.YSortCameraGroup = lambda _: None
    # level_module.PlayerMagic = lambda _: None
    # level_module.Upgrade = lambda _: None
    # level_module.UI = lambda: None

    # pygame.font.Font = lambda _, __: None

    # Level.create_map = lambda self: None
    # Level.create_layouts = lambda self: None
    # Level.player = None

    level = Level("Sky", lambda: None)

    enemy = level.spawn_enemy("A", (0, 0))

    assert enemy.monster_name == "akuma"

def test_spawn_eagle():
    pygame.init()
    pygame.display.set_mode((100, 100))

    level = Level("Sky", lambda: None)

    enemy = level.spawn_enemy("14", (0, 0))

    assert enemy.monster_name == "eagle"

def test_spawn_snow_skeleton():
    pygame.init()
    pygame.display.set_mode((100, 100))

    level = Level("Sky", lambda: None)

    enemy = level.spawn_enemy("ske", (0, 0))

    assert enemy.monster_name == "snow_skeleton"

def test_spawn_random_skeleton():
    pygame.init()
    pygame.display.set_mode((100, 100))

    level = Level("Hell", lambda: None)

    enemy = level.spawn_enemy("ske", (0, 0))

    assert enemy.monster_name in ("snow_skeleton", "fire_skeleton", "thunder_skeleton")

def test_spawn_nukekubi():
    pygame.init()
    pygame.display.set_mode((100, 100))

    level = Level("Sky", lambda: None)

    enemy = level.spawn_enemy("nukekubi", (0, 0))

    assert enemy.monster_name == "nukekubi"