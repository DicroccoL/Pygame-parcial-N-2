import pygame
from Constantes import *
from Funciones import *

pygame.init()

boton_suma = crear_elemento_juego("mas.webp", 60, 60, 420, 200)
boton_resta = crear_elemento_juego("menos.webp", 60, 60, 20, 200)
boton_volver = crear_elemento_juego("textura_respuesta.png", 100, 40, 10, 10)
boton_mute = crear_elemento_juego("mute.png", 60, 60, 220, 300)
fondo = pygame.transform.scale(pygame.image.load("fondo.jpg"), PANTALLA)

def mostrar_ajustes(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict) -> str:
    retorno = "ajustes"

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_suma["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_musica"] <= 95:
                        datos_juego["volumen_musica"] += 5
                        CLICK_SONIDO.play()
                    else:
                        ERROR_SONIDO.play()
                elif boton_resta["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_musica"] > 0:
                        datos_juego["volumen_musica"] -= 5
                        CLICK_SONIDO.play()
                    else:
                        ERROR_SONIDO.play()
                elif boton_mute["rectangulo"].collidepoint(evento.pos):
                    datos_juego["volumen_musica"] = 0
                    CLICK_SONIDO.play()
                elif boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    retorno = "menu"

    pantalla.blit(fondo, (0, 0))  # Fondo completo

    pantalla.blit(boton_suma["superficie"], boton_suma["rectangulo"])
    pantalla.blit(boton_resta["superficie"], boton_resta["rectangulo"])
    pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])
    pantalla.blit(boton_mute["superficie"], boton_mute["rectangulo"])

    mostrar_texto(pantalla, f"{datos_juego['volumen_musica']} %", (200, 200), FUENTE_VOLUMEN, COLOR_NEGRO)
    mostrar_texto(boton_volver["superficie"], "VOLVER", (5, 5), FUENTE_RESPUESTA, COLOR_BLANCO)

    # Barra de volumen visual
    barra_base = pygame.Rect(100, 250, 300, 20)
    barra_relleno = pygame.Rect(100, 250, 3 * datos_juego["volumen_musica"], 20)

    pygame.draw.rect(pantalla, (200, 200, 200), barra_base)  # Fondo de la barra (gris)
    pygame.draw.rect(pantalla, (0, 255, 0), barra_relleno)  # Barra rellena (verde)

    return retorno
