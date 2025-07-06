import pygame
import os
from Constantes import *
from Funciones import *

pygame.init()

boton_volver = crear_elemento_juego("textura_respuesta.png", 100, 40, 10, 10)
fondo = pygame.transform.scale(pygame.image.load("fondo.jpg"), PANTALLA)

def mostrar_rankings(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], lista_rankings: list) -> str:
    retorno = "rankings"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    retorno = "menu"

    pantalla.blit(fondo, (0, 0))  # Fondo completo

    # Cuadrado blanco semi-transparente para mejorar visibilidad del texto
    overlay = pygame.Surface((PANTALLA[0] - 100, PANTALLA[1] - 170))  # Tamaño del recuadro
    overlay.set_alpha(200)  # Transparencia (0 a 255)
    overlay.fill((255, 255, 255))  # Blanco
    pantalla.blit(overlay, (50, 80))  # Posición del recuadro

    pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])

    import json

    rankings = []
    if os.path.exists("partidas.json"):
        try:
            with open("partidas.json", "r", encoding="utf-8") as f:
                partidas = json.load(f)
                rankings = sorted(partidas, key=lambda x: x["puntuacion"], reverse=True)
        except (FileNotFoundError, json.JSONDecodeError):
            rankings = []

    y = 100
    for indice, entrada in enumerate(rankings[:10], start=1):
        nombre = entrada.get("nombre", "Sin nombre")
        puntaje = entrada.get("puntuacion", 0)
        fecha = entrada.get("fecha", "")
        mostrar_texto(pantalla, f"TOP {indice}: {nombre} - {puntaje} pts - {fecha}", (60, y), FUENTE_RESPUESTA, COLOR_NEGRO)
        y += 30

    mostrar_texto(boton_volver["superficie"], "VOLVER", (5, 5), FUENTE_RESPUESTA, COLOR_BLANCO)

    return retorno
