import pygame
import sys
import time

"""
    Classe usada para guardar as configurações e status de objetos do jogo
    Para sempre compartilhar as mesmas informações entre os objetos, seguimos o padrão de Singleton, ou seja,
    só existe uma instância dessa classe, e ela é acessada por todos os objetos que precisam de suas informações
"""

class GameStats:
    def __init__(self):
        # Dificuldade do jogo
        self.DIFFICULT = 1
        self.DIFFICULT_VALUES_VARIATION_PERCENTAGE = .5

        self.set_difficult_time = 0
        self.set_difficult_cooldown = .5

        # Status do jogador, que são inicializados de acordo com a dificuldade
        # A entidade Player é instanciada sempre que um Level novo é carregado, então para não perder os status do jogador
        # quando ele morre ou passa de level, salvamos os status do jogador em um dict e inicializamos o jogador com esses
        # status salvos
        self.player_stats = {
                        'health': self.calculate_property_by_difficult(100), 
                        'mana': 60, 
                        'attack': self.calculate_property_by_difficult(10), 
                        'speed': 2, 
                        'magic': self.calculate_property_by_difficult(4)
                    }
        self.player_stats_backup = self.player_stats.copy() # Usado para resetar os status do jogador quando ele morre
        self.player_exp = 100
        self.player_health = self.player_stats["health"]
        self.player_mana = self.player_stats['mana']
        
        # Quantidade de inimigos que aparecem no level
        self.enemies_amount = 0

        # Diz se o jogo está em tela cheia ou não
        self.is_fullscreen = False
        self.toggle_fullscreen_time = 0

    def reset_player_stats(self):
        # Reseta os status do jogador para os valores iniciais
        self.player_stats = self.player_stats_backup.copy()
        self.player_exp = 100
        self.player_health = self.player_stats["health"]

    def calculate_property_by_difficult(self, prop, invert_sign=False):
        """
        Retorna o valor de uma propriedade + ou - uma variação de acordo com a dificuldade

        Calcula o valor de uma propriedade do jogador de acordo com a dificuldade
        Os números das propriedades podem variar de acordo com a variável DIFFICULT_VALUES_VARIATION_PERCENTAGE
        Ex: se o valor base de uma propriedade é 100, e a variacao é 50%, então o valor da propriedade pode variar de 50 a 150

        Multiplicamos a variação por DIFFICULT para que o sinal da variação mude de acordo com a dificulade
        Ex: se estiver no modo fácil, a variação será positiva, se estiver no modo difícil, a variação será negativa
        com o exemplo anterior, se estiver no modo fácil (e invert_sign for False), a propriedade irá aumentar para 150
        se estiver no modo difícil (e invert_sign for False), a propriedade irá diminuir para 50

        Se invert_sign for True, inverte o sinal da variação mais uma vez
        Isso ocorre para podermos usar a mesma função tanto para as propriedades do player quanto para as propriedades dos inimigos,
        que são calculadas de forma inversa
        Ex: Se o a vida dos inimigos e do player são 100, mas estivermos no modo fácil, a vida do player aumenta para 150
        e a vida dos inimigos diminui para 50
        """
        return prop + ( prop * self.DIFFICULT_VALUES_VARIATION_PERCENTAGE * self.DIFFICULT * (-1 if invert_sign else 1) )

    def set_difficult(self):
        # Muda a dificuldade do jogo
        if time.time() - self.set_difficult_time > self.set_difficult_cooldown:
            self.DIFFICULT += 1

            if self.DIFFICULT > 1:
                self.DIFFICULT = -1 # Se a dificuldade for maior que 1, volta para -1, fazendo assim um ciclo de dificuldades (fácil, médio, difícil)
            self.set_difficult_time = time.time() # Reseta o tempo para que a dificuldade não mude muito rápido
    
    def close(self):
        pygame.quit()
        sys.exit()

    def get_difficult(self):
        return self.DIFFICULT
    
    def change_screen(self):
        # Alterna entre tela cheia e janela
        curr_time = pygame.time.get_ticks()

        if curr_time -self.toggle_fullscreen_time >= 500:
            pygame.display.toggle_fullscreen()
            self.is_fullscreen = not self.is_fullscreen # Alterna o status de tela cheia, se estiver em tela cheia, passa para janela e vice-versa
            self.toggle_fullscreen_time = curr_time

gameStats = GameStats()