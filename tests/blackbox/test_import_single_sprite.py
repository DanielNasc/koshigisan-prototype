import pygame

import sys
import os
sys.path.append(os.path.dirname(__file__) + '/../..')

from support.sprites_support import import_a_single_sprite 
from support.sprites_support import import_positions


# Testes para a função import_a_single_sprite

# O que deve ser testado:
#     - Se a função importa corretamente um sprite
#     - Se a função escala o sprite em x vezes, onde x é o parâmetro scale
#     - Se a função retorna None quanto os parâmetros quando path é inválido
#     - Se a função retorna None quanto os parâmetros quando scale é inválido

def test_import_a_single_sprite():
    # Testa se a função importa corretamente um sprite
    pygame.init()
    pygame.display.set_mode((100, 100))

    # Importa um sprite
    sprite = import_a_single_sprite("/tests/blackbox/img/test.png")

    # Verifica se o sprite foi importado corretamente e é uma instancia de Surface
    assert sprite is not None
    assert isinstance(sprite, pygame.Surface)

def test_import_a_single_sprite_scale():
    # Testa se a função escala o sprite em x vezes, onde x é o parâmetro scale
    pygame.init()
    pygame.display.set_mode((100, 100))

    # Importa um sprite com escala normal
    sprite = import_a_single_sprite("/tests/blackbox/img/test.png")

    # Importa um sprite com escala 2x
    sprite2 = import_a_single_sprite("/tests/blackbox/img/test.png", 2)

    sprite3 = import_a_single_sprite("/tests/blackbox/img/test.png", 0.00001)

    # Verifica se o sprite foi importado corretamente e é uma instancia de Surface
    assert sprite is not None
    assert isinstance(sprite, pygame.Surface)
    assert sprite2 is not None
    assert isinstance(sprite2, pygame.Surface)

    # Verifica se o sprite foi escalado corretamente
    assert sprite.get_width() == sprite2.get_width() / 2
    assert sprite.get_height() == sprite2.get_height() / 2

    assert sprite.get_width() == sprite3.get_width() / 0.00001
    assert sprite.get_height() == sprite3.get_height() / 0.00001

"""
    Utilizando partição de equivalência, vamos dividir os tipos de daodos em 2 grupos, com relação ao parâmetro scale:
        - Valores válidos: inteiros e floats positivos e None
        - Valores inválidos: inteiros e floats negativos, strings, listas, tuplas, dicionários, booleanos, etc

    Com base nisso, vamos testar ao menos 1 valor válido e 1 valor inválido para cada tipo de dado
"""

def test_import_a_single_sprite_invalid_scale():
    # Testa se a função retorna None quanto os parâmetros quando scale é inválido
    pygame.init()
    pygame.display.set_mode((100, 100))

    # Importa um sprite
    sprite = import_a_single_sprite("/tests/blackbox/img/test.png", True)

    # apenas com esse teste, já cobrimos todos os tipos de dados inválido
    # pois como testamos com True, que é um tipo diferente de int e float, já cobrimos todos os tipos de dados

    assert sprite is None

def test_import_a_single_sprite_invalid_scale_limits():
    # Testa por meio da análise de valores limites, se a função retorna 
    # None quanto os parâmetros quando path é inválido
    pygame.init()
    pygame.display.set_mode((100, 100))

    # Importa um sprite
    # Como a função só aceita valores maiores do que 0, só precisamos testar 3 valores: -1, 0 e 1.
    sprites = [
        import_a_single_sprite("/tests/blackbox/img/test.png", -.000001),
        import_a_single_sprite("/tests/blackbox/img/test.png", 0),
        import_a_single_sprite("/tests/blackbox/img/test.png", .000001),
    ]

    # Verifica se o sprite foi importado corretamente e é uma instancia de Surface
    for sprite in sprites:
        assert sprite is None

def test_import_a_single_sprite_invalid_path():
    # Testa se a função retorna None quanto os parâmetros quando path é inválido
    pygame.init()
    pygame.display.set_mode((100, 100))

    # Importa um sprite
    sprite = import_a_single_sprite(True)

    assert sprite is None

def test_import_position():
    # Testa se a função retorna corretamente um array
    pygame.init()
    pygame.display.set_mode((100, 100))

    # Importa o mapa
    position_map = []
    position_map = import_positions("tests/blackbox/position/teste.csv")

    assert position_map is not None

def test_import_position_invalid_path():
    # Testa se a função retorna None quanto os parâmetros quando o path é inválido
    pygame.init()
    pygame.display.set_mode((100, 100))

    # Importa o mapa
    position_map = []
    position_map = import_positions(True)

    assert position_map is None

