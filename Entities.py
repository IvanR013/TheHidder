import math, pygame, random
from interface import  *


'''
Módulo de desarrollo de las entidades del juego y su lógica.

'''


class Enemy:

    def __init__(self, x, y, patrol_area, speed, vision_range, orientation: int, sprite_sheet_path, num_frames):
        """
        :Constructor: 

        Crea un enemigo en las coordenadas (x, y) con velocidad y puntos de patrullaje definidos en su instancia.
        Args:
            x (float): Coordenada inicial en el eje x.
            y (float): Coordenada inicial en el eje y.
            patrol_area (tuple): Área de patrullaje ((min_x, min_y), (max_x, max_y)).
            speed (float): Velocidad del enemigo.
            vision_range (float): Rango de visión del enemigo para detectar al jugador.
        
        """
        # Atributos físicos
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 50
        self.height = 50
        
        # Atributos de Inteligencia
        self.vision_range = vision_range
        self.patrol_area = patrol_area
        self.patroling = True #Flag para saber si está patrullando
        self.current_target = None
        self.orientation = orientation
        self.vision_angle = 90

        # Atributos de Animación
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.num_frames = num_frames
        self.frame_width = self.sprite_sheet.get_width() // num_frames
        self.frame_height = self.sprite_sheet.get_height() // 4

        self.animations = self.load_frames()
        self.current_frame = 0 # Frame de la animación
        self.direction = 0 # Dirección actual de la animación
        self.animation_speed = 0.1 # velocidad de animación

    def load_frames(self):

        '''
        :Load Frames:

        - Separa las animaciones en una lista de 4 elementos (para los 4 lados a los que se puede mover el personaje.)
        
        '''

        animations = [[] for i in range(4)]

        for direction in range(4):
            for frame in range(self.num_frames):

                rect=pygame.Rect(frame * self.frame_width, direction * self.frame_height, self.frame_width, self.frame_height)

                frame_image = self.sprite_sheet.subsurface(rect)
                animations[direction].append(frame_image)
        
        return animations
    
    def update_animation(self):
        '''
        :Update Animation:

        - Obtiene la lista del método `load_frames()` y reinicia las animaciones en bucle siempre que se alcance el último cuadro para que se dé ese efecto de animación.
       
         Además, en `self.current_frame += self.animation_speed` el frame actual se actualiza a una velocidad dada por `self.animation_speed` que es fraccionaria. Esto no es casual, y se hace para que los frames transcurran más lentamente, generando esa suavidad en la animación del personaje.
        '''
        self.current_frame += self.animation_speed
        
        if self.current_frame >= len(self.animations[self.direction]):

            self.current_frame = 0 


    def move_towards(self, target_x, target_y):
        """
        Mueve al enemigo hacia una posición objetivo limitada por su velocidad máxima.

        Este método ajusta la posición `self.x` y `self.y` del enemigo en dirección a las coordenadas
        `target_x` y `target_y` en función de una velocidad máxima (`self.velocidad`). Si la distancia
        en uno de los ejes es menor que `self.velocidad`, el enemigo se mueve directamente a esa
        coordenada, asegurando que no sobrepase la posición del objetivo.

        Parameters:
        - target_x (float): Coordenada x del objetivo.
        - target_y (float): Coordenada y del objetivo.

        Logic:
        - Calcula la distancia en x (`dx`) e y (`dy`) hacia el objetivo.
        - Mueve el enemigo en cada eje con incrementos de `self.velocidad`, hasta llegar o estar 
          suficientemente cerca del objetivo.

        """
        dx = target_x - self.x
        dy = target_y - self.y

        if abs(dx) > self.speed:
        
            self.x += self.speed if dx > 0 else - self.speed
        
        else:
            
            self.x = target_x
        
        if abs(dy) > self.speed:

            self.y += self.speed if dy > 0 else - self.speed
       
        else:
       
            self.y = target_y


    def patrol(self):

        """
        :Patrol:

        - Permite al enemigo merodear patrullando aleatoreamente dentro de una zona definida.
        - Si el enemigo se encuentra a 5 unidades de su objetivo o éste no tiene un valor,
        Se llama al método `get_random_patrol_point()` que genera aleatoriamente coords y ése será su
        próximo destino (siempre que no vea al jugador).
        """
        
        if self.patroling:
            # Si no hay un objetivo asignado o el enemigo ha llegado al objetivo,
            # se genera un nuevo punto aleatorio dentro de la zona de patrullaje.
            
            if self.current_target is None or \
                 abs(self.x - self.current_target[0]) < 5 and abs(self.y - self.current_target[1]) < 5:
           
                 self.current_target = self.get_random_patrol_point()

           
            # Mover al enemigo hacia el objetivo.
            self.move_towards(self.current_target[0], self.current_target[1])
        
    def detect_player(self, player_x, player_y):
        """
        Detecta si el jugador está dentro del rango de visión del enemigo.

        Args:
            player_x (float): Coordenada x del jugador.
            player_y (float): Coordenada y del jugador.

        Returns:
            bool: True si el jugador está dentro del rango de visión, de lo contrario False.
        """
    
        # Calcular la distancia entre el enemigo y el jugador
        distance = math.sqrt((self.x - player_x)**2 + (self.y - player_y)**2)
    
         # Verificar si el jugador está fuera del rango de visión
        if distance > self.vision_range:
             
            return False  # El jugador está fuera del rango de visión
    
         # Calcular el ángulo entre la dirección del enemigo y la posición del jugador
        dx = player_x - self.x
        dy = player_y - self.y
    
         # Ángulo entre el enemigo y el jugador
        angle_to_player = math.atan2(dy, dx)
    
        # Asegurarse de que el ángulo del enemigo está en el rango adecuado (relativo a su orientación)
        # El enemigo tiene una orientación, que es el ángulo al cual está mirando
        # Se considera que la orientación del enemigo está en grados, por ejemplo:
        # self.orientation es el ángulo en grados, en el que el enemigo está mirando (0° = derecha, 90° = arriba)
    
        # Convertir la orientación del enemigo en radianes
        enemy_orientation = math.radians(self.orientation)  # Asumimos que self.orientation tiene el valor de la orientación actual
    
        # Calcular el rango de visión relativo al enemigo
        left_bound = enemy_orientation - math.radians(self.vision_angle / 2)
        right_bound = enemy_orientation + math.radians(self.vision_angle / 2)
    
         # Normalizar el ángulo hacia el jugador
        player_angle = math.radians(angle_to_player)
    
        # Verificar si el jugador está dentro del campo de visión
        if left_bound <= player_angle <= right_bound:
        
            return True  # El jugador está dentro del campo de visión
    
        return False  # El jugador no está dentro del campo de visión    
    
    def update_behavior(self, player_x, player_y):

        '''
         Actualiza el comportamiento del enemigo: patrulla o persigue al jugador.

        Args:
            player_x (float): Coordenada x del jugador.
            player_y (float): Coordenada y del jugador.

        Si el enemigo detecta al jugador entrando en su rango de visión,
        Este deja de patrullar (`self.patroling = False`) y activa `move_towards(player_x, player_y)`, dirigiéndose hacia la posición del jugador.
        De lo contrario, vuelve a su estado de patrulla (`self.patroling = True`), y vuelve a moverse aleatoreamente `(patrol())`. 
        
        '''
        # Primero verificamos si el enemigo detecta al jugador (prioridad a la persecución)
        if self.detect_player(player_x, player_y):
        
            self.patroling = False  # Deja de patrullar
        
            self.move_towards(player_x, player_y)  # Persigue al jugador
        
            return  # Detiene el flujo si está persiguiendo al jugador

        # Si no está persiguiendo al jugador, verificamos si está fuera de su área de patrullaje
        
        if not self.is_within_patrol_area():
        
            self.patroling = True  # Regresa a patrullar
        
            self.patrol()  # Inicia el patrullaje
        
            return  # Detiene el flujo si está fuera de su área

        # Si está dentro de su área de patrullaje y no hay jugador cerca, continúa patrullando
        self.patroling = True
        self.patrol()  # Sigue patrullando si no hay jugador cerca

    def get_random_patrol_point(self):

        '''
        Genera un punto aleatorio dentro del área de patrullaje.
        Retorna una tupla (x, y) que representa el próximo objetivo de patrullaje.
        
        '''
        patrol_x_min, patrol_y_min = self.patrol_area[0]
        patrol_x_max, patrol_y_max = self.patrol_area[1]

        x = random.randint(patrol_x_min, patrol_x_max)
        y = random.randint(patrol_y_min, patrol_y_max)

        return(x, y)


    def is_within_patrol_area(self):
        """
        Verifica si el enemigo está dentro de su área de patrullaje
        """
        patrol_x_min, patrol_y_min = self.patrol_area[0]
        patrol_x_max, patrol_y_max = self.patrol_area[1]

        # Verificar si el enemigo está dentro de los límites del área de patrullaje

        return patrol_x_min <= self.x <= patrol_x_max and patrol_y_min <= self.y <= patrol_y_max    
    

    def DrawGame(self, screen):
        """
        Dibuja al enemigo en la pantalla utilizando las coordenadas y la animación actual.

        Args:
        
        screen (pygame.Surface): La superficie de la pantalla de Pygame donde se dibuja el enemigo.
        """
        # Obtener el frame actual de la animación
        frame = self.animations[self.direction][int(self.current_frame)]

        # Dibujar el frame en las coordenadas (self.x, self.y)
        screen.blit(frame, (self.x, self.y))


        
