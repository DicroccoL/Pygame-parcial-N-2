from modules.Funciones import *
from modules.Constantes import *

def aplicar_bomba(pregunta: dict, lista_respuestas: list, respuestas_visibles: list) -> list:
    """
    Aplica el comodín 'bomba' ocultando dos respuestas incorrectas.

    Args:
        pregunta (dict): Diccionario con los datos de la pregunta actual.
        lista_respuestas (list): Lista de botones de respuesta (diccionarios con 'superficie' y 'rectangulo').
        respuestas_visibles (list): Lista de booleanos que indican qué respuestas están visibles.

    Returns:
        list: Lista actualizada de respuestas visibles (con solo una correcta y una incorrecta mostradas).
    """
    correcta = pregunta["respuesta_correcta"]
    opciones = [i for i in range(1, 5)]
    opciones.remove(correcta)
    incorrecta_mostrada = random.choice(opciones)
    visibles = [correcta, incorrecta_mostrada]

    for i in range(len(lista_respuestas)):
        if (i + 1) not in visibles:
            lista_respuestas[i]["superficie"].fill((0, 0, 0, 0)) 
            respuestas_visibles[i] = False
    return respuestas_visibles

def activar_x2(datos_juego: dict) -> None:
    """
    Activa el comodín 'x2' en el diccionario de datos del juego.

    Marca que el siguiente acierto otorgará el doble de puntos.

    Args:
        datos_juego (dict): Diccionario con el estado actual del juego.
    """
    datos_juego["comodines_usados"]["x2"] = True 
    datos_juego["x2_activado"] = True             

def aplicar_efecto_x2(datos_juego: dict) -> int:
    """
    Calcula la puntuación a otorgar según si el comodín 'x2' está activo.

    Args:
        datos_juego (dict): Diccionario con el estado actual del juego.

    Returns:
        int: Puntuación a sumar (doble si el comodín 'x2' está activado).
    """
    match datos_juego["comodines_usados"].get("x2"):
        case True:
            return PUNTUACION_ACIERTO * 2
        case _:
            return PUNTUACION_ACIERTO
