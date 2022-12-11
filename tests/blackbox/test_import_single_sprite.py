import pygame

import sys
import os
sys.path.append(os.path.dirname(__file__) + '/../..')

from support.sprites_support import import_a_single_sprite


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

    # Verifica se o sprite foi importado corretamente e é uma instancia de Surface
    assert sprite is not None
    assert isinstance(sprite, pygame.Surface)
    assert sprite2 is not None
    assert isinstance(sprite2, pygame.Surface)

    # Verifica se o sprite foi escalado corretamente
    assert sprite.get_width() == sprite2.get_width() / 2
    assert sprite.get_height() == sprite2.get_height() / 2

def test_import_a_single_sprite_invalid_path():
    # Testa se a função retorna None quanto os parâmetros quando path é inválido
    pygame.init()
    pygame.display.set_mode((100, 100))

    # Importa um sprite
    sprites = [
        import_a_single_sprite(1),
        import_a_single_sprite(1.0),
        import_a_single_sprite(True),
        import_a_single_sprite(False),
        import_a_single_sprite(None),
        import_a_single_sprite([]),
        import_a_single_sprite({}),
        import_a_single_sprite(()),
        import_a_single_sprite("  "),
    ]

    # Verifica se o sprite foi importado corretamente e é uma instancia de Surface
    for sprite in sprites:
        assert sprite is None

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