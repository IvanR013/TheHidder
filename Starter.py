import pygame, sys

from Menus import MainMenu, PauseMenu

from Main import Game

class AppGame:

    def __init__(self, width = 800, height = 700):
        
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Juego pausado")

        self.menu_status = MainMenu(self)
        self.GameStatus = Game(self)
        self.Pause_status = PauseMenu(self)

        self.current_status = self.menu_status


    def ChangeStatus(self, new_status):

        self.current_status = new_status

    def run_app(self):

        while True:
            
            self.current_status.EventManager()
            self.current_status.Updates()
            self.current_status.DrawGame()
            pygame.display.flip()



# Ejecutar la aplicación del juego

if __name__ == "__main__":

    app = AppGame()

    app.run()  