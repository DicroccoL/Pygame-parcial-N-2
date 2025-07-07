import pygame
pygame.init()

COLOR_BLANCO = (255,255,255)
COLOR_NEGRO = (0,0,0)
COLOR_VERDE = (0,255,0)
COLOR_ROJO = (255,0,0)
COLOR_AZUL = (0,0,255)
COLOR_VIOLETA = (134,23,219)
ANCHO = 500
ALTO = 600
PANTALLA = (ANCHO,ALTO)
FPS = 30

BOTON_JUGAR = 0
BOTON_CONFIG = 1
BOTON_PUNTUACIONES = 2
BOTON_SALIR = 3

ANCHO_PREGUNTA = 350
ALTO_PREGUNTA = 150
ANCHO_BOTON = 250
ALTO_BOTON = 60
ANCHO_CUADRO = 250
ALTO_CUADRO = 50
ANCHO_BOTON_MENU = 250
ALTO_BOTON_MENU = 60
TAMAÑO_BOTON_VOLUMEN = (60,60)
TAMAÑO_BOTON_VOLVER = (100,40)
CLICK_SONIDO = pygame.mixer.Sound("./modules/assets/sounds/click.mp3")
ERROR_SONIDO = pygame.mixer.Sound("./modules/assets/sounds/error.mp3")
FUENTE_PREGUNTA = pygame.font.Font("./modules/assets/font/fuente.otf",22)
FUENTE_RESPUESTA = pygame.font.Font("./modules/assets/font/fuente.otf",17)
FUENTE_TEXTO = pygame.font.Font("./modules/assets/font/fuente.otf",25)
FUENTE_VOLUMEN = pygame.font.Font("./modules/assets/font/fuente.otf",50)
FUENTE_CUADRO_TEXTO = pygame.font.Font("./modules/assets/font/fuente.otf",25)
FUENTE_RANKING = pygame.font.Font("./modules/assets/font/fuente.otf",22)

BOTON_JUGAR = 0

CANTIDAD_VIDAS = 3
PUNTUACION_ACIERTO = 100
PUNTUACION_ERROR = 25
CANTIDAD_TIEMPO = 60