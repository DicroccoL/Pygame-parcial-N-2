import pygame
pygame.init()

# Colores RGB usados en la interfaz
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_VERDE = (0, 255, 0)
COLOR_ROJO = (255, 0, 0)
COLOR_AZUL = (0, 0, 255)
COLOR_VIOLETA = (134, 23, 219)

# Tamaño de pantalla
ANCHO = 1280
ALTO = 720
PANTALLA = (ANCHO, ALTO)

# Frames por segundo
FPS = 30

# Índices de los botones del menú principal
BOTON_JUGAR = 0
BOTON_CONFIG = 1
BOTON_PUNTUACIONES = 2
BOTON_SALIR = 3

# Dimensiones de los distintos elementos de UI
ANCHO_PREGUNTA = 350
ALTO_PREGUNTA = 150
ANCHO_BOTON = 250
ALTO_BOTON = 60
ANCHO_CUADRO = 250
ALTO_CUADRO = 50
ANCHO_BOTON_MENU = 250
ALTO_BOTON_MENU = 60
TAMAÑO_BOTON_VOLUMEN = (60, 60)
TAMAÑO_BOTON_VOLVER = (100, 40)

# Sonidos del juego
CLICK_SONIDO = pygame.mixer.Sound("./modules/assets/sounds/click.mp3")
ERROR_SONIDO = pygame.mixer.Sound("./modules/assets/sounds/error.mp3")

# Fuentes del juego
FUENTE_PREGUNTA = pygame.font.Font("./modules/assets/font/fuente.otf", 22)
FUENTE_RESPUESTA = pygame.font.Font("./modules/assets/font/fuente.otf", 17)
FUENTE_TEXTO = pygame.font.Font("./modules/assets/font/fuente.otf", 25)
FUENTE_VOLUMEN = pygame.font.Font("./modules/assets/font/fuente.otf", 50)
FUENTE_CUADRO_TEXTO = pygame.font.Font("./modules/assets/font/fuente.otf", 25)
FUENTE_RANKING = pygame.font.Font("./modules/assets/font/fuente.otf", 22)

# Reglas del juego
CANTIDAD_VIDAS = 3               # Vidas iniciales del jugador
PUNTUACION_ACIERTO = 100         # Puntos por respuesta correcta
PUNTUACION_ERROR = 25            # Puntos descontados por error
CANTIDAD_TIEMPO = 60             # Tiempo inicial en segundos
