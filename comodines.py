import pygame
import random
from Constantes import *

# Estado inicial de los comodines
comodines_usados = {
    "bomba": False,
    "x2": False,
    "doble_chance": False,
    "pasar": False
}

# Banderas para efectos de comodines
puntaje_doble = False
doble_chance_activada = False
pasar_activado = False

def dibujar_comodines(pantalla, fuente):
    nombres = [
        ("BOMBA", "bomba"),
        ("X2", "x2"),
        ("DOBLE", "doble_chance"),
        ("PASAR", "pasar")
    ]

    for i, (label, key) in enumerate(nombres):
        y = 100 + i * 100
        estado = comodines_usados[key]
        color_boton = (180, 0, 0) if estado else (0, 100, 200)
        pygame.draw.rect(pantalla, color_boton, (20, y, 110, 50))
        texto = fuente.render(label, True, (255, 255, 255))
        pantalla.blit(texto, (30, y + 10))

def detectar_click_comodin(mouse_pos):
    x, y = mouse_pos
    if x < 150:
        index = (y - 100) // 100
        if 0 <= index < 4:
            return ["bomba", "x2", "doble_chance", "pasar"][index]
    return None

def aplicar_comodin(nombre, opciones, respuesta_correcta):
    global puntaje_doble, doble_chance_activada, pasar_activado
    if nombre == "bomba":
        return eliminar_dos_incorrectas(opciones, respuesta_correcta)
    elif nombre == "x2":
        puntaje_doble = True
    elif nombre == "doble_chance":
        doble_chance_activada = True
    elif nombre == "pasar":
        pasar_activado = True
    return opciones

def eliminar_dos_incorrectas(opciones, respuesta_correcta):
    """Elimina 2 opciones incorrectas, manteniendo solo la correcta y una incorrecta"""
    # Encontrar opciones incorrectas
    incorrectas = [o for o in opciones if o != respuesta_correcta]
    
    # Si hay al menos 2 incorrectas, eliminar 2 y mantener 1
    if len(incorrectas) >= 2:
        # Elegir 1 incorrecta al azar para mantener
        incorrecta_a_mantener = random.choice(incorrectas)
        # Devolver la respuesta correcta y una incorrecta (las otras 2 se eliminan)
        return [respuesta_correcta, incorrecta_a_mantener]
    
    # Si hay menos de 2 incorrectas, devolver todas las opciones
    return opciones

def resetear_comodines():
    global comodines_usados, puntaje_doble, doble_chance_activada, pasar_activado
    comodines_usados = {k: False for k in comodines_usados}
    puntaje_doble = False
    doble_chance_activada = False
    pasar_activado = False

def resetear_efectos_temporales():
    """Resetea solo los efectos temporales después de una pregunta"""
    global puntaje_doble
    puntaje_doble = False
    # doble_chance_activada NO se resetea aquí, se resetea cuando se usa completamente