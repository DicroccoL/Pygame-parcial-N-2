"""
Módulo del menú principal del juego.

Este archivo contiene la función `mostrar_menu` que gestiona la pantalla principal del menú,
permitiendo al jugador acceder a las distintas secciones del juego: Jugar, Rankings, Ajustes o Salir.
"""

import pygame
from modules.Constantes import *
from modules.Funciones import *

# Inicialización de Pygame y recursos visuales
pygame.init()
lista_botones = crear_botones_menu()
fondo_menu = pygame.transform.scale(pygame.image.load("./modules/assets/images/fondo_del_menu.jpg"), PANTALLA)


def mostrar_menu(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event]) -> str:
    """
    Muestra el menú principal y gestiona la navegación entre secciones del juego.

    Args:
        pantalla (pygame.Surface): Superficie principal donde se renderiza el menú.
        cola_eventos (list[pygame.event.Event]): Lista de eventos de entrada.

    Returns:
        str: El próximo estado del juego.
    """
    retorno = "menu"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i in range(len(lista_botones)):
                if lista_botones[i]["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()  # Sonido al hacer clic
                    if i == BOTON_JUGAR:
                        retorno = "juego"
                    elif i == BOTON_PUNTUACIONES:
                        retorno = "rankings"
                    elif i == BOTON_CONFIG:
                        retorno = "ajustes"
                    else:
                        retorno = "salir"

    pantalla.blit(fondo_menu, (0, 0))
    for boton in lista_botones:
        pantalla.blit(boton["superficie"], boton["rectangulo"])

    mostrar_texto(lista_botones[BOTON_JUGAR]["superficie"], "JUGAR", (70, 20), FUENTE_TEXTO, COLOR_BLANCO)
    mostrar_texto(lista_botones[BOTON_PUNTUACIONES]["superficie"], "RANKINGS", (70, 20), FUENTE_TEXTO, COLOR_BLANCO)
    mostrar_texto(lista_botones[BOTON_CONFIG]["superficie"], "AJUSTES", (70, 20), FUENTE_TEXTO, COLOR_BLANCO)
    mostrar_texto(lista_botones[BOTON_SALIR]["superficie"], "SALIR", (70, 20), FUENTE_TEXTO, COLOR_BLANCO)

    return retorno
