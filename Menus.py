'''
The Hidder Test INDEV

Módulo donde se manejan los menúes principales del juego.

'''

import pygame

import sys

from interface import GameStatus



class MainMenu(GameStatus):

    def __init__(self, game):

        super().__init__(game)

    def EventManager(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    self.game.ChangeStatus(self.game.Game_status)

    
    def Updates(self):
        
       pass
    
    
    def DrawGame(self):

        self.game.display.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Presioná ENTER para jugar", True, (255, 255, 255))
        self.game.display.blit(text, (self.game.width // 2 - text.get_width() // 2, self.game.height // 2 - text.get_height() // 2))





class PauseMenu(GameStatus):

    def __init__(self, game):

        super().__init__(game)

    def EventManager(self):
        """
        Maneja los eventos en el estado de pausa, como reanudar el juego.

        Nótese que, en este caso; ESC también se asigna para reanudar el juego además de pausarlo.
        """
        for event in pygame.event.get():
           
            if event.type == pygame.QUIT:
            
                pygame.quit()
            
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
            
                if event.key == pygame.K_ESCAPE:  # "ESC" para reanudar
            
                    self.game.ChangeStatus(self.game.game_status)

    def Updates(self):
    
        pass


    def DrawGame(self):
        """
        Dibuja el mensaje de pausa en la pantalla.
        """
        self.game.display.fill((50, 50, 50))
        font = pygame.font.Font(None, 74)
        text = font.render("Juego Pausado", True, (255, 255, 255))
        self.game.display.blit(text, (self.game.width // 2 - text.get_width() // 2, self.game.height // 2 - text.get_height() // 2))
        
        
    