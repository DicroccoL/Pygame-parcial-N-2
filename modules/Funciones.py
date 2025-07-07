import random
from modules.Constantes import *
import pygame

def mostrar_texto(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, False, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

#GENERAL
def mezclar_lista(lista_preguntas:list) -> None:
    random.shuffle(lista_preguntas)

#GENERAL
def reiniciar_estadisticas(datos_juego:dict) -> None:
    datos_juego["puntuacion"] = 0
    datos_juego["vidas"] = CANTIDAD_VIDAS
    datos_juego["nombre"] = ""
    datos_juego["tiempo_restante"] = CANTIDAD_TIEMPO

#GENERAL
def verificar_respuesta(datos_juego:dict, pregunta:dict, respuesta:int) -> bool:
    if respuesta == pregunta["respuesta_correcta"]:
        datos_juego["puntuacion"] += PUNTUACION_ACIERTO
        datos_juego["racha"] += 1

        if datos_juego["racha"] % 5 == 0:
            datos_juego["vidas"] += 1
            datos_juego["mensaje_vida"]["mostrar"] = True
            datos_juego["mensaje_vida"]["contador"] = 30 
            datos_juego["tiempo_restante"] += 15

        return True
    else:
        datos_juego["vidas"] -= 1
        datos_juego["puntuacion"] -= PUNTUACION_ERROR
        datos_juego["racha"] = 0
        return False


def crear_elemento_juego(textura:str,ancho:int,alto:int,pos_x:int,pos_y:int) -> dict:
    elemento_juego = {}
    elemento_juego["superficie"] = pygame.transform.scale(pygame.image.load(textura),(ancho,alto))
    elemento_juego["rectangulo"] = elemento_juego["superficie"].get_rect()
    elemento_juego["rectangulo"].x = pos_x
    elemento_juego["rectangulo"].y = pos_y
    
    return elemento_juego

def limpiar_superficie(elemento_juego:dict,textura:str,ancho:int,alto:int) -> None:
    elemento_juego["superficie"] =  pygame.transform.scale(pygame.image.load(textura),(ancho,alto))
    
def obtener_respuesta_click(lista_respuestas:list,pos_click:tuple):
    respuesta = None
    
    for i in range(len(lista_respuestas)):
        if lista_respuestas[i]["rectangulo"].collidepoint(pos_click):
            respuesta = i + 1
    
    return respuesta

def cambiar_pregunta(lista_preguntas:list,indice:int,caja_pregunta:dict,lista_respuestas:list) -> dict:
    pregunta_actual = lista_preguntas[indice]
    limpiar_superficie(caja_pregunta,"./modules/assets/images/textura_pregunta.png",ANCHO_PREGUNTA,ALTO_PREGUNTA)
    for i in range(len(lista_respuestas)):
        limpiar_superficie(lista_respuestas[i],"./modules/assets/images/textura_respuesta.png",ANCHO_BOTON,ALTO_BOTON)
    
    return pregunta_actual

def crear_botones_menu() -> list:
    lista_botones = []

    cantidad_botones = 4
    espaciado = 20
    alto_total = cantidad_botones * ALTO_BOTON_MENU + (cantidad_botones - 1) * espaciado
    pos_y = (ALTO - alto_total) // 2  # Centrado vertical
    pos_x = (ANCHO - ANCHO_BOTON_MENU) // 2  # Centrado horizontal

    for _ in range(cantidad_botones):
        boton = crear_elemento_juego("./modules/assets/images/fondo_menu.png", ANCHO_BOTON_MENU, ALTO_BOTON_MENU, pos_x, pos_y)
        lista_botones.append(boton)
        pos_y += ALTO_BOTON_MENU + espaciado

    return lista_botones

def crear_respuestas(textura:str,ancho:int,alto:int,pos_x:int,pos_y:int,cantidad_respuestas:int) -> list:
    lista_respuestas = []
    
    for i in range(cantidad_respuestas):
        boton_respuesta = crear_elemento_juego(textura,ancho,alto,pos_x,pos_y)
        lista_respuestas.append(boton_respuesta)
        pos_y += 80
    
    return lista_respuestas

def manejar_texto(cuadro_texto: dict, tecla_presionada: str, bloc_mayus: int, datos_juego: dict) -> None:
    nombre_actual = datos_juego["nombre"]

    # Borrar letra
    if tecla_presionada == "backspace" and len(nombre_actual) > 0:
        datos_juego["nombre"] = nombre_actual[:-1]
        limpiar_superficie(cuadro_texto, "./modules/assets/images/textura_respuesta.png", ANCHO_CUADRO, ALTO_CUADRO)

    # Solo permitir letras
    elif len(tecla_presionada) == 1 and tecla_presionada.isalpha():
        if len(nombre_actual) < 12:
            CLICK_SONIDO.play()
            if bloc_mayus == 8192 or bloc_mayus & pygame.KMOD_SHIFT:
                datos_juego["nombre"] += tecla_presionada.upper()
            else:
                datos_juego["nombre"] += tecla_presionada.lower()