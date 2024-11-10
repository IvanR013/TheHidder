'''
The Hidder Test INDEV

Archivo donde se manejan los eventos principales del juego.

'''
import pygame

import sys

from interface import *

from Menus import MainMenu, PauseMenu

from Entities import Enemy

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

        

class Game(GameStatus):

    def __init__(self, game):
        
        super().__init__(game)

        self.enemies = [
            Enemy(x=400, y=100, patrol_area=(350, 450), speed=2, vision_range=200, orientation= 0)
        
        ]

        self.player_pos = [100, 100]

    def EventManager(self):

         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN: #Escuchamos el evento de presionar una tecla.
                
                if event.key == pygame.K_ESCAPE:  #Asignamos "ESC" para pausar
                    
                    self.game.ChangeStatus(self.game.pause_status) #Una vez que presionamos la tecla asignada, llamamos mediante la variable "pause_status" a la clase que controla el menú de pausa.

  
    def Updates(self):
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
        
            self.player_pos[1] -= 5
        
        if keys[pygame.K_DOWN]:
        
            self.player_pos[1] += 5
        
        if keys[pygame.K_LEFT]:
        
            self.player_pos[0] -= 5
        
        if keys[pygame.K_RIGHT]:
        
            self.player_pos[0] += 5

        
        # Actualizar la lógica del enemigo
        self.enemies[0].update_behavior(self.player_pos)  # Actualiza el comportamiento del enemigo.
        
   
    def DrawGame(self):
        self.game.display.fill((0, 128, 255))  # Limpiar pantalla con el color de fondo

         # Dibujar el enemigo (accedemos al primer enemigo de la lista)
        self.enemies[0].draw(self.game.display)

        # Dibujar el jugador
        pygame.draw.circle(self.game.display, (255, 0, 0), self.player_pos, 20)


 