import pygame
import os
from modules.Constantes import *
from modules.Funciones import *
import json
from datetime import datetime
import random

pygame.init()

# Elementos visuales de la pantalla final del juego
cuadro_texto = crear_elemento_juego("./modules/assets/images/textura_respuesta.png", ANCHO_CUADRO, ALTO_CUADRO, 480, 150)
fondo = pygame.transform.scale(pygame.image.load("./modules/assets/images/game over.png"), PANTALLA)
boton_volver = crear_elemento_juego("./modules/assets/images/textura_respuesta.png", 100, 40, 10, 10)
boton_guardar = crear_elemento_juego("./modules/assets/images/textura_respuesta.png", 100, 40, 550, 210)

def mostrar_fin_juego(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict, lista_rankings: list) -> str:
    """
    Muestra la pantalla de finalización del juego, permite al jugador ingresar su nombre
    y guardar su puntuación en un archivo JSON si el nombre es válido.

    Parámetros:
    - pantalla (pygame.Surface): Superficie principal donde se dibuja todo el contenido.
    - cola_eventos (list): Lista de eventos de pygame capturados.
    - datos_juego (dict): Diccionario con información actual del juego (puntos, nombre, flags de guardado).
    - lista_rankings (list): Lista de rankings (no utilizada en esta función, futura expansión).

    Retorna:
    - str: Estado de transición, puede ser "terminado", "salir" o "menu".
    """
    retorno = "terminado"

    # Manejo de eventos
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    datos_juego["guardado"] = False
                    datos_juego["guardado_exito"] = False
                    datos_juego["nombre"] = ""
                    retorno = "menu"

                elif boton_guardar["rectangulo"].collidepoint(evento.pos):
                    nombre = datos_juego["nombre"]

                    # Validación: mínimo 3 letras, solo caracteres alfabéticos
                    if len(nombre) >= 3 and all(letra.isalpha() for letra in nombre):
                        entrada = {
                            "nombre": nombre,
                            "puntuacion": datos_juego["puntuacion"],
                            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }

                        try:
                            with open("./modules/partidas.json", "r", encoding="utf-8") as f:
                                partidas = json.load(f)
                        except (FileNotFoundError, json.JSONDecodeError):
                            partidas = []

                        partidas.append(entrada)

                        with open("./modules/partidas.json", "w", encoding="utf-8") as f:
                            json.dump(partidas, f, indent=4, ensure_ascii=False)

                        datos_juego["guardado"] = True
                        datos_juego["guardado_exito"] = True
                    else:
                        datos_juego["guardado"] = True
                        datos_juego["guardado_exito"] = False

        elif evento.type == pygame.KEYDOWN:
            tecla_presionada = pygame.key.name(evento.key)
            bloc_mayus = pygame.key.get_mods()
            manejar_texto(cuadro_texto, tecla_presionada, bloc_mayus, datos_juego)

    # Renderizado visual
    pantalla.blit(fondo, (0, 0))
    pantalla.blit(cuadro_texto["superficie"], cuadro_texto["rectangulo"])
    mostrar_texto(pantalla, f"Usted obtuvo: {datos_juego['puntuacion']} puntos", (440, 55), FUENTE_TEXTO, COLOR_BLANCO)

    pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])
    mostrar_texto(boton_volver["superficie"], "MENU", (5, 10), FUENTE_RESPUESTA, COLOR_BLANCO)

    pantalla.blit(boton_guardar["superficie"], boton_guardar["rectangulo"])
    mostrar_texto(boton_guardar["superficie"], "GUARDAR", (5, 10), FUENTE_RESPUESTA, COLOR_BLANCO)

    # Mensajes según resultado del intento de guardado
    if datos_juego.get("guardado_exito"):
        mostrar_texto(pantalla, "¡Guardado!", (560, 290), FUENTE_RESPUESTA, COLOR_BLANCO)
    elif datos_juego.get("guardado") and not datos_juego.get("guardado_exito"):
        mostrar_texto(pantalla, "Nombre inválido (solo letras, mín. 3 )", (440, 133), FUENTE_RESPUESTA, "#F20606")

    # Refresca cuadro de texto
    limpiar_superficie(cuadro_texto, "./modules/assets/images/textura_respuesta.png", ANCHO_CUADRO, ALTO_CUADRO)

    # Muestra nombre ingresado en tiempo real con cursor intermitente
    if datos_juego["nombre"] != "":
        if random.randint(1, 2) == 1:
            mostrar_texto(cuadro_texto["superficie"], f"{datos_juego['nombre']}|", (10, 10), FUENTE_CUADRO_TEXTO, COLOR_BLANCO)
        else:
            mostrar_texto(cuadro_texto["superficie"], f"{datos_juego['nombre']}", (10, 10), FUENTE_CUADRO_TEXTO, COLOR_BLANCO)
    else:
        mostrar_texto(cuadro_texto["superficie"], "INGRESE SU NOMBRE", (10, 15), FUENTE_RESPUESTA, "#736767")

    return retorno
