import pygame
import os
from modules.Constantes import *
from modules.Funciones import *

pygame.init()

# Botón para volver al menú
boton_volver = crear_elemento_juego("./modules/assets/images/textura_respuesta.png", 100, 40, 10, 10)

# Fondo del menú de rankings
fondo = pygame.transform.scale(pygame.image.load("./modules/assets/images/fondo_del_menu.jpg"), PANTALLA)

def mostrar_rankings(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], lista_rankings: list) -> str:
    """
    Muestra la pantalla de rankings con los puntajes más altos guardados en un archivo JSON.

    Parámetros:
    - pantalla (pygame.Surface): Superficie principal donde se dibuja el contenido.
    - cola_eventos (list[pygame.event.Event]): Lista de eventos capturados por pygame.
    - lista_rankings (list): Lista de rankings pasada al módulo (no usada directamente, reservada para futuro uso).

    Retorna:
    - str: Indica a qué vista debe cambiar el programa ("menu", "salir", o "rankings" si permanece).
    """
    retorno = "rankings"

    # Manejo de eventos
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    retorno = "menu"

    # Dibuja fondo
    pantalla.blit(fondo, (0, 0))

    # Dibuja un recuadro blanco semitransparente para los rankings
    overlay = pygame.Surface((PANTALLA[0] - 100, PANTALLA[1] - 170))
    overlay.set_alpha(200)
    overlay.fill((255, 255, 255))
    pantalla.blit(overlay, (50, 80))

    # Dibuja botón volver
    pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])
    mostrar_texto(boton_volver["superficie"], "VOLVER", (5, 5), FUENTE_RESPUESTA, COLOR_BLANCO)

    # Carga rankings desde archivo JSON
    import json
    rankings = []
    if os.path.exists("./modules/partidas.json"):
        try:
            with open("./modules/partidas.json", "r", encoding="utf-8") as f:
                partidas = json.load(f)
                rankings = sorted(partidas, key=lambda x: x["puntuacion"], reverse=True)
        except (FileNotFoundError, json.JSONDecodeError):
            rankings = []

    # Muestra el top 10 en pantalla
    y = 100
    for indice, entrada in enumerate(rankings[:10], start=1):
        nombre = entrada.get("nombre", "Sin nombre")
        puntaje = entrada.get("puntuacion", 0)
        fecha = entrada.get("fecha", "")
        mostrar_texto(
            pantalla,
            f"TOP {indice}: {nombre} - {puntaje} pts - {fecha}",
            (60, y),
            FUENTE_RESPUESTA,
            COLOR_NEGRO
        )
        y += 30

    return retorno
