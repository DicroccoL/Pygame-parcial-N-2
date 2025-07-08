import pygame
from modules.Constantes import *
from modules.Funciones import *

pygame.init()

# Crear botones con sus imágenes, tamaños y posiciones
boton_suma = crear_elemento_juego("./modules/assets/images/mas.webp", 60, 60, 710, 300)
boton_resta = crear_elemento_juego("./modules/assets/images/menos.webp", 60, 60, 510, 300)
boton_volver = crear_elemento_juego("./modules/assets/images/textura_respuesta.png", 100, 40, 10, 10)
boton_mute = crear_elemento_juego("./modules/assets/images/mute.png", 60, 60, 610, 400)

# Fondo de ajustes
fondo = pygame.transform.scale(pygame.image.load("./modules/assets/images/fondo_del_menu.jpg"), (1280, 720))


def mostrar_ajustes(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict) -> str:
    """
    Muestra la pantalla de ajustes y maneja la lógica de interacción con los botones de volumen.

    Permite aumentar, disminuir, silenciar y visualizar el nivel de volumen.
    También ofrece un botón para volver al menú principal.

    Parameters
    ----------
    pantalla : pygame.Surface
        Superficie principal donde se renderiza la pantalla.
    cola_eventos : list[pygame.event.Event]
        Lista de eventos capturados (mouse, teclado, etc.).
    datos_juego : dict
        Diccionario que contiene el estado actual del juego, incluyendo 'volumen_musica'.

    Returns
    -------
    str
        El estado siguiente del juego: 'ajustes', 'menu' o 'salir'.
    """
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

    pantalla.blit(fondo, (0, 0))

    # Dibujar botones
    pantalla.blit(boton_suma["superficie"], boton_suma["rectangulo"])
    pantalla.blit(boton_resta["superficie"], boton_resta["rectangulo"])
    pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])
    pantalla.blit(boton_mute["superficie"], boton_mute["rectangulo"])

    # Dibujar cuadro del porcentaje
    cuadro_ancho, cuadro_alto = 120, 50
    cuadro_x = (1280 - cuadro_ancho) // 2
    cuadro_y = 180

    superficie_cuadro = pygame.Surface((cuadro_ancho, cuadro_alto), pygame.SRCALPHA)
    superficie_cuadro.fill((0, 0, 0, 180))
    pantalla.blit(superficie_cuadro, (cuadro_x, cuadro_y))

    texto = f"{datos_juego['volumen_musica']} %"
    texto_render = FUENTE_VOLUMEN.render(texto, True, COLOR_BLANCO)
    texto_rect = texto_render.get_rect(center=(cuadro_x + cuadro_ancho // 2, cuadro_y + cuadro_alto // 2))
    pantalla.blit(texto_render, texto_rect)

    mostrar_texto(boton_volver["superficie"], "VOLVER", (5, 5), FUENTE_RESPUESTA, COLOR_BLANCO)

    # Dibujar barra de volumen
    barra_base = pygame.Rect((1280 - 300) // 2, 270, 300, 20)
    barra_relleno = pygame.Rect((1280 - 300) // 2, 270, 3 * datos_juego["volumen_musica"], 20)

    pygame.draw.rect(pantalla, (200, 200, 200), barra_base)
    pygame.draw.rect(pantalla, (0, 255, 0), barra_relleno)

    return retorno
