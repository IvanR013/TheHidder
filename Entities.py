import math, pygame, random


'''
Módulo de desarrollo de las entidades del juego y su lógica.

'''


class Enemy():

    def __init__(self, x, y, patrol_area, speed):
        """
        Crea un enemigo en las coordenadas (x, y) con velocidad y puntos de patrullaje definidos.
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 50
        self.height = 50
        self.color = (255, 0, 0)  # Color del enemigo (rojo) 
        
        self.patrol_area = patrol_area
        self.patroling = True #Flag para saber si está patrullando
        self.current_target = None

    def move_towards(self, target_x, target_y):

        dx = target_x - self.x
        dy = target_y - self.y

        if abs(dx) > self.velocidad:
        
            self.x += self.velocidad if dx > 0 else - self.velocidad
        
        else:
            
            self.x = target_x
        
        if abs(dy) > self.velocidad:

            self.y += self.velocidad if dy > 0 else - self.velocidad
       
        else:
       
            self.y = target_y


    def patrol(self):
        """Movimiento de patrullaje aleatorio dentro de una zona definida."""
        
        if self.patroling:
            # Si no hay un objetivo asignado o el enemigo ha llegado al objetivo,
            # se genera un nuevo punto aleatorio dentro de la zona de patrullaje.
            
            if self.current_target is None or \
                 abs(self.x - self.current_target[0]) < 5 and abs(self.y - self.current_target[1]) < 5:
           
                 self.current_target = self.get_random_patrol_point()

           
            # Mover al enemigo hacia el objetivo.
            self.move_towards(self.current_target[0], self.current_target[1])
        
        
        







        