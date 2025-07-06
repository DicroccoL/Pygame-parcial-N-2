import pygame
from Constantes import *
from Funciones import *

pygame.init()

# Crear botones con sus imágenes, tamaños y posiciones
boton_suma = crear_elemento_juego("mas.webp", 60, 60, 420, 200)
boton_resta = crear_elemento_juego("menos.webp", 60, 60, 20, 200)
boton_volver = crear_elemento_juego("textura_respuesta.png", 100, 40, 10, 10)
boton_mute = crear_elemento_juego("mute.png", 60, 60, 220, 300)

# Fondo escalado a 500x500 (PANTALLA)
fondo = pygame.transform.scale(pygame.image.load("fondo.jpg"), (500, 500))


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

    # Rectángulo negro semitransparente para resaltar el texto del volumen
    cuadro_ancho, cuadro_alto = 120, 50
    cuadro_x = (500 - cuadro_ancho) // 2  # centro horizontal pantalla 500x500
    cuadro_y = 180  # vertical fijo para que quede arriba de la barra

    superficie_cuadro = pygame.Surface((cuadro_ancho, cuadro_alto), pygame.SRCALPHA)
    superficie_cuadro.fill((0, 0, 0, 180))  # negro semitransparente
    pantalla.blit(superficie_cuadro, (cuadro_x, cuadro_y))

    # Texto porcentaje volumen centrado en ese cuadro
    texto = f"{datos_juego['volumen_musica']} %"
    texto_render = FUENTE_VOLUMEN.render(texto, True, COLOR_BLANCO)
    texto_rect = texto_render.get_rect(center=(cuadro_x + cuadro_ancho // 2, cuadro_y + cuadro_alto // 2))
    pantalla.blit(texto_render, texto_rect)

    # Texto en botón volver
    mostrar_texto(boton_volver["superficie"], "VOLVER", (5, 5), FUENTE_RESPUESTA, COLOR_BLANCO)

    # Barra de volumen visual
    barra_base = pygame.Rect(100, 250, 300, 20)
    barra_relleno = pygame.Rect(100, 250, 3 * datos_juego["volumen_musica"], 20)

    pygame.draw.rect(pantalla, (200, 200, 200), barra_base)  # Fondo de la barra (gris)
    pygame.draw.rect(pantalla, (0, 255, 0), barra_relleno)  # Barra rellena (verde)

    return retorno
