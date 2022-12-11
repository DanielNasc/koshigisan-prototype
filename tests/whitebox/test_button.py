import pygame

import sys
import os
sys.path.append(os.path.dirname(__file__) + '/../..')

from level.menu.button import Button

"""
Testes para a classe Button

O que deve ser testado:
    - Se o botão executa a função passada como parâmetro
    - Se o botão muda de cor quando o mouse está sobre ele
    - Se o botão permanece com a cor padrão quando o mouse não está sobre ele
"""

def test_button_action():
    # Testa se o botão executa a função passada como parâmetro

    pygame.init()
    pygame.display.set_mode((100, 100))
    font = pygame.font.SysFont("Arial", 20)

    # Cria uma função de teste
    executed = False
    def mock_function():
        nonlocal executed
        executed = True

    # Cria um botão com a função de teste
    button = Button((0,0), 100, 100, "Test", (255, 255, 255), font, (0, 0, 0), [], None, (0, 0, 0), (100, 100, 100), mock_function)

    # Modifica funções do pygame para simular o clique do mouse
    pygame.mouse.get_pressed = lambda: (True, False, False)
    pygame.mouse.get_pos = lambda: (0, 0)

    # Atualiza o botão
    button.update()

    # Verifica se a função foi executada
    assert executed

def test_button_hover():
    # Testa se o botão muda de cor quando o mouse está sobre ele

    pygame.init()
    pygame.display.set_mode((100, 100))
    font = pygame.font.SysFont("Arial", 20)

    # Cria um botão
    button = Button((0,0), 100, 100, "Test", (255, 255, 255), font, (0, 0, 0), [], None, (0, 0, 0), (100, 100, 100), None)

    # Modifica funções do pygame para simular o mouse sobre o botão
    pygame.mouse.get_pressed = lambda: (False, False, False)
    pygame.mouse.get_pos = lambda: (0, 0)

    # Atualiza o botão
    button.update()

    # Verifica se a cor do botão foi alterada
    assert button.top_color == (100, 100, 100)

def test_button_not_hover():
    # Testa se o botão permanece com a cor padrão quando o mouse não está sobre ele

    pygame.init()
    pygame.display.set_mode((100, 100))
    font = pygame.font.SysFont("Arial", 20)

    # Cria um botão
    button = Button((0,0), 100, 100, "Test", (255, 255, 255), font, (0, 0, 0), [], None, (0, 0, 0), (100, 100, 100), None)

    # Colocar o botao em hover e depois tirar

    # Modifica funções do pygame para simular o mouse sobre o botão
    pygame.mouse.get_pressed = lambda: (False, False, False)
    pygame.mouse.get_pos = lambda: (0, 0)

    # Atualiza o botão
    button.update()

    # Modifica funções do pygame para simular o mouse fora do botão
    pygame.mouse.get_pressed = lambda: (False, False, False)
    pygame.mouse.get_pos = lambda: (200, 200)

    # Atualiza o botão
    button.update()

    # Verifica se a cor do botão não foi alterada
    assert button.top_color == (255, 255, 255)