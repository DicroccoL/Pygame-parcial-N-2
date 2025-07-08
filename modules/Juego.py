"""
Módulo principal del juego Preguntados.

Este módulo inicializa la ventana principal del juego y contiene la función `mostrar_juego`,
que gestiona el loop principal durante el estado de juego, incluyendo la lógica de eventos,
comodines, respuestas y actualización de pantalla.
"""

import pygame
from modules.Constantes import *
from modules.Preguntas import *
from modules.Funciones import *
from modules.comodines import *

# Inicialización de Pygame
pygame.init()
pygame.display.set_caption("PREGUNTADOS")
icono = pygame.image.load("./modules/assets/images/icono.png")
pygame.display.set_icon(icono)
pantalla = pygame.display.set_mode(PANTALLA)

# Variables de estado del juego
datos_juego = {
    "puntuacion": 0,
    "vidas": CANTIDAD_VIDAS,
    "nombre": "",
    "tiempo_restante": CANTIDAD_TIEMPO,
    "comodines_usados": {"bomba": False, "x2": False,"doble_chance": False,"pasar": False },
    "doble_chance_activado": False,
    "intento_doble": False,
    "pasar_activado": False,
}

# Fondo y elementos iniciales
fondo_pantalla = pygame.transform.scale(pygame.image.load("./modules/assets/images/fondo.jpg"), PANTALLA)
caja_pregunta = crear_elemento_juego(
    "./modules/assets/images/textura_pregunta.png",
    ANCHO_PREGUNTA, ALTO_PREGUNTA,
    (ANCHO - ANCHO_PREGUNTA) // 2, 50
)

# Botones de respuesta
x_respuesta = (ANCHO - ANCHO_BOTON) // 2
y_respuesta_inicial = 250
lista_respuestas = crear_respuestas(
    "./modules/assets/images/textura_respuesta.png",
    ANCHO_BOTON, ALTO_BOTON,
    x_respuesta, y_respuesta_inicial, 4
)

#Saco las coordenadas para poder centrar cada comodin con cada respuesta
y_bomba = y_respuesta_inicial
y_x2 = y_respuesta_inicial + ALTO_BOTON + 8
y_doble = y_x2 + ALTO_BOTON + 8
y_pasar = y_doble + ALTO_BOTON + 8
# Botones de comodines
boton_bomba = crear_elemento_juego("./modules/assets/images/bomba.png", 40, 40, ANCHO - 485, ALTO - 460)
boton_x2 = crear_elemento_juego("./modules/assets/images/x2.png", 40, 40, ANCHO - 486, ALTO - 378)
boton_doble_chance = crear_elemento_juego("./modules/assets/images/doble_chance.png", 40, 40, ANCHO - 485, ALTO - 300)
boton_pasar = crear_elemento_juego("./modules/assets/images/pasar.png", 40, 40, ANCHO - 485, ALTO - 220)
# ordenar preguntas al azar
mezclar_lista(lista_preguntas)

corriendo = True
reloj = pygame.time.Clock()
evento_tiempo = pygame.USEREVENT
pygame.time.set_timer(evento_tiempo, 1000)

def mostrar_juego(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict) -> str:
    """
    Muestra y gestiona la pantalla principal del juego.

    Esta función:
    - Dibuja la interfaz de juego (pregunta, respuestas, puntaje, tiempo, etc.).
    - Maneja los eventos del mouse, incluyendo selección de respuestas y activación de comodines.
    - Aplica lógica del juego como puntajes, rachas, vidas y temporizador.

    Args:
        pantalla (pygame.Surface): Superficie principal donde se dibuja el juego.
        cola_eventos (list[pygame.event.Event]): Lista de eventos capturados por pygame.
        datos_juego (dict): Diccionario con el estado actual del juego.

    Returns:
        str: El próximo estado de pantalla ("juego", "terminado", "salir").
    """
    if "racha" not in datos_juego:
        datos_juego["racha"] = 0
    if "mensaje_vida" not in datos_juego:
        datos_juego["mensaje_vida"] = {"mostrar": False, "contador": 0}
    if "respuestas_visibles" not in datos_juego:
        datos_juego["respuestas_visibles"] = [True, True, True, True]

    respuestas_visibles = datos_juego["respuestas_visibles"]
    retorno = "juego"
    pregunta_actual = lista_preguntas[datos_juego['indice']]

    # Fin de juego por vidas o tiempo
    if datos_juego["vidas"] == 0 or datos_juego["tiempo_restante"] == 0:
        retorno = "terminado"

    # Procesamiento de eventos
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton_bomba["rectangulo"].collidepoint(evento.pos) and not datos_juego["comodines_usados"]["bomba"]:
                CLICK_SONIDO.play() 
                datos_juego["respuestas_visibles"] = aplicar_bomba(pregunta_actual, lista_respuestas, respuestas_visibles)
                datos_juego["comodines_usados"]["bomba"] = True
            elif boton_x2["rectangulo"].collidepoint(evento.pos) and not datos_juego["comodines_usados"]["x2"]:
                CLICK_SONIDO.play()
                activar_x2(datos_juego)
            elif boton_doble_chance["rectangulo"].collidepoint(evento.pos) and not datos_juego["comodines_usados"]["doble_chance"]:
                CLICK_SONIDO.play()
                activar_doble_chance(datos_juego)
            elif boton_pasar["rectangulo"].collidepoint(evento.pos) and not datos_juego["comodines_usados"]["pasar"]:
                CLICK_SONIDO.play()
                usar_pasar_pregunta(datos_juego)
                datos_juego['indice'] += 1
                if datos_juego['indice'] == len(lista_preguntas):
                    mezclar_lista(lista_preguntas)
                    datos_juego['indice'] = 0
                pregunta_actual = cambiar_pregunta(lista_preguntas, datos_juego['indice'], caja_pregunta, lista_respuestas)
                datos_juego["respuestas_visibles"] = [True, True, True, True]
                respuestas_visibles = datos_juego["respuestas_visibles"]
            else:
                # Manejo de clics en respuestas
                respuesta = obtener_respuesta_click(lista_respuestas, evento.pos)
                if respuesta is not None:
                    avanzar_pregunta = False

                    if datos_juego.get("doble_chance_activado", False):
                        if verificar_respuesta(datos_juego, pregunta_actual, respuesta):
                            CLICK_SONIDO.play()
                            datos_juego["doble_chance_activado"] = False
                            datos_juego["intento_doble"] = False
                            avanzar_pregunta = True
                        else:
                            if not datos_juego.get("intento_doble", False):
                                ERROR_SONIDO.play()
                                datos_juego["intento_doble"] = True
                            else:
                                ERROR_SONIDO.play()
                                datos_juego["vidas"] -= 1
                                datos_juego["puntuacion"] -= PUNTUACION_ERROR
                                datos_juego["racha"] = 0
                                datos_juego["doble_chance_activado"] = False
                                datos_juego["intento_doble"] = False
                                avanzar_pregunta = True
                    else:
                        if verificar_respuesta(datos_juego, pregunta_actual, respuesta):
                            CLICK_SONIDO.play()
                        else:
                            ERROR_SONIDO.play()
                        avanzar_pregunta = True

                    if avanzar_pregunta:
                        datos_juego['indice'] += 1
                        if datos_juego['indice'] == len(lista_preguntas):
                            mezclar_lista(lista_preguntas)
                            datos_juego['indice'] = 0
                        pregunta_actual = cambiar_pregunta(lista_preguntas, datos_juego['indice'], caja_pregunta, lista_respuestas)
                        datos_juego["respuestas_visibles"] = [True, True, True, True]
                        respuestas_visibles = datos_juego["respuestas_visibles"]
        elif evento.type == evento_tiempo:
            datos_juego["tiempo_restante"] -= 1

    # Dibujo en pantalla
    pantalla.blit(fondo_pantalla, (0, 0))
    pantalla.blit(caja_pregunta["superficie"], caja_pregunta["rectangulo"])

    for i in range(len(lista_respuestas)):
        if respuestas_visibles[i]:
            pantalla.blit(lista_respuestas[i]["superficie"], lista_respuestas[i]["rectangulo"])

    mostrar_texto(caja_pregunta["superficie"], pregunta_actual["pregunta"], (20, 40), FUENTE_PREGUNTA, COLOR_NEGRO)

    # Mostrar respuestas visibles
    respuestas_keys = ["respuesta_1", "respuesta_2", "respuesta_3", "respuesta_4"]
    for i in range(4):
        if respuestas_visibles[i]:
            mostrar_texto(lista_respuestas[i]["superficie"], pregunta_actual[respuestas_keys[i]], (20, 20), FUENTE_RESPUESTA, COLOR_BLANCO)

    # Mostrar HUD
    mostrar_texto(pantalla, f"VIDAS: {datos_juego['vidas']}", (10, 10), FUENTE_TEXTO)
    mostrar_texto(pantalla, f"PUNTUACION: {datos_juego['puntuacion']}", (10, 40), FUENTE_TEXTO)
    mostrar_texto(pantalla, f"TIEMPO: {datos_juego['tiempo_restante']} s", (ANCHO - 220, 10), FUENTE_TEXTO)

    # Mensaje de bonus por racha
    if datos_juego["mensaje_vida"]["mostrar"]:
        mostrar_texto(pantalla, "¡Vida extra por racha!", (ANCHO // 2 - 150, ALTO - 140), FUENTE_RESPUESTA, COLOR_BLANCO)
        mostrar_texto(pantalla, "Bonus +15s por responder bien!", (ANCHO // 2 - 150, ALTO - 120), FUENTE_RESPUESTA, COLOR_BLANCO)
        datos_juego["mensaje_vida"]["contador"] -= 1
        if datos_juego["mensaje_vida"]["contador"] <= 0:
            datos_juego["mensaje_vida"]["mostrar"] = False

    # Dibuja la barra negra detrás de los comodines
    superficie_transparente = pygame.Surface((60, 300), pygame.SRCALPHA)
    color_negro_transparente = (0, 0, 0, 150)
    pygame.draw.rect(superficie_transparente, color_negro_transparente, pygame.Rect(0, 0, 60, 300), border_radius=8)
    pantalla.blit(superficie_transparente, (ANCHO - 495, ALTO - 470))
                        

    # Mostrar botones de comodines si no se usaron
    if not datos_juego["comodines_usados"]["bomba"]:
        pantalla.blit(boton_bomba["superficie"], boton_bomba["rectangulo"])
    if not datos_juego["comodines_usados"]["x2"]:
        pantalla.blit(boton_x2["superficie"], boton_x2["rectangulo"])
    if not datos_juego["comodines_usados"]["doble_chance"]:
        pantalla.blit(boton_doble_chance["superficie"], boton_doble_chance["rectangulo"])
    if not datos_juego["comodines_usados"]["pasar"]:
        pantalla.blit(boton_pasar["superficie"], boton_pasar["rectangulo"])
    
    return retorno
