from modules.Funciones import *
from modules.Juego import *

def aplicar_bomba(pregunta: dict, lista_respuestas: list, respuestas_visibles: list) -> list:
    
    correcta = pregunta["respuesta_correcta"]
    opciones = [i for i in range(1, 5)]
    opciones.remove(correcta)
    incorrecta_mostrada = random.choice(opciones)
    visibles = [correcta, incorrecta_mostrada]

    for i in range(len(lista_respuestas)):
        if (i + 1) not in visibles:
            lista_respuestas[i]["superficie"].fill((0, 0, 0, 0))  # borra visualmente
            respuestas_visibles[i] = False
    return respuestas_visibles
