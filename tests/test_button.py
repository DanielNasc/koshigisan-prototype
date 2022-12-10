import unittest
from unittest.mock import Mock
import pygame

import sys
import os
sys.path.append(os.path.dirname(__file__) + '/..')

from level.menu.button import Button

"""
Testes para a classe Button

O que deve ser testado:
    - Se o botão executa a função passada como parâmetro
    - Se o botão muda de cor quando o mouse está sobre ele
    - Se o botão permanece com a cor padrão quando o mouse não está sobre ele
"""

class TestButton(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.font = pygame.font.SysFont('Arial', 30)

    def test_button_action(self):
        # testa se o botão executa a função passada como parâmetro
        mock_func = Mock()
        button = Button(
            (0, 0),
            100,
            100,
            'Test',
            (255, 255, 255),
            self.font,
            (0, 0, 0),
            [],
            0,
            (0, 0, 0),
            (0, 0, 0),
            mock_func
        )
    
        # mock pygame.mouse.get_pressed
        pygame.mouse.get_pressed = Mock(return_value=(1, 0, 0))
        # mock pygame.mouse.get_pos
        pygame.mouse.get_pos = Mock(return_value=(0, 0))
        # mock pygame.display.get_surface
        pygame.display.get_surface = Mock(return_value=self.screen)

        button.update()
        mock_func.assert_called_once()

    def test_hover(self):
        # testa se o botão muda de cor quando o mouse está sobre ele
        button = Button(
            (0, 0),
            100,
            100,
            'Test',
            (255, 255, 255),
            self.font,
            (0, 0, 0),
            [],
            0,
            (0, 0, 0),
            (1, 1, 1),
            lambda: None
        )
    
        # mock pygame.mouse.get_pos
        pygame.mouse.get_pos = Mock(return_value=(0, 0))
        # mock pygame.display.get_surface
        pygame.display.get_surface = Mock(return_value=self.screen)

        button.update()
        self.assertEqual(button.top_color, (1, 1, 1))

    def test_default_color(self):
        # testa se o botão permanece com a cor padrão quando o mouse não está sobre ele
        button = Button(
            (0, 0),
            100,
            100,
            'Test',
            (255, 255, 255),
            self.font,
            (0, 0, 0),
            [],
            0,
            (0, 0, 0),
            (1, 1, 1),
            lambda: None
        )
    
        # mock pygame.mouse.get_pos
        pygame.mouse.get_pos = Mock(return_value=(101, 101))
        # mock pygame.display.get_surface
        pygame.display.get_surface = Mock(return_value=self.screen)

        button.update()
        self.assertEqual(button.top_color, (255, 255, 255))


if __name__ == '__main__':
    unittest.main()