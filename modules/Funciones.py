import random
from modules.Constantes import *
import pygame
from modules.comodines import aplicar_efecto_x2

def mostrar_texto(surface, text, pos, font, color=pygame.Color('black')):
    """
    Muestra un texto multilínea en la superficie especificada, respetando los saltos de línea y el ancho máximo.

    Args:
        surface (pygame.Surface): Superficie donde se renderiza el texto.
        text (str): Texto a mostrar.
        pos (tuple): Posición inicial (x, y).
        font (pygame.font.Font): Fuente para renderizar.
        color (pygame.Color, optional): Color del texto. Por defecto negro.
    """
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, False, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]
        y += word_height

def mezclar_lista(lista_preguntas: list) -> None:
    """
    Mezcla aleatoriamente la lista de preguntas.

    Args:
        lista_preguntas (list): Lista de preguntas a mezclar.
    """
    random.shuffle(lista_preguntas)

def reiniciar_estadisticas(datos_juego: dict) -> None:
    """
    Reinicia los valores del juego a su estado inicial.

    Args:
        datos_juego (dict): Diccionario que contiene los datos del juego.
    """
    datos_juego["puntuacion"] = 0
    datos_juego["vidas"] = CANTIDAD_VIDAS
    datos_juego["nombre"] = ""
    datos_juego["tiempo_restante"] = CANTIDAD_TIEMPO
    datos_juego["comodines_usados"] = {"bomba": False, "x2": False,"doble_chance": False,"pasar": False}
    datos_juego["doble_chance_activado"] = False
    datos_juego["intento_doble"] = False
    datos_juego["pasar_activado"] = False   

def verificar_respuesta(datos_juego: dict, pregunta: dict, respuesta: int) -> bool:
    """
    Verifica si la respuesta es correcta y actualiza el estado del juego.

    Args:
        datos_juego (dict): Diccionario con el estado del juego.
        pregunta (dict): Pregunta actual.
        respuesta (int): Respuesta seleccionada (1 a 4).

    Returns:
        bool: True si es correcta, False si es incorrecta.
    """
    if respuesta == pregunta["respuesta_correcta"]:
        if datos_juego.get("x2_activado"):
            puntos = PUNTUACION_ACIERTO * 2
            datos_juego["x2_activado"] = False
        else:
            puntos = PUNTUACION_ACIERTO

        datos_juego["puntuacion"] += puntos
        datos_juego["racha"] += 1

        if datos_juego["racha"] % 5 == 0:
            datos_juego["vidas"] += 1
            datos_juego["mensaje_vida"]["mostrar"] = True
            datos_juego["mensaje_vida"]["contador"] = 30
            datos_juego["tiempo_restante"] += 15

        return True
    else:
        # Si el doble chance está activado, no penalizar en el primer intento
        if datos_juego.get("doble_chance_activado", False) and not datos_juego.get("intento_doble", False):
            # Primer intento incorrecto con doble chance - no penalizar
            return False
        else:
            # Respuesta incorrecta normal o segundo intento con doble chance
            datos_juego["vidas"] -= 1
            datos_juego["puntuacion"] -= PUNTUACION_ERROR
            datos_juego["racha"] = 0
            return False

def crear_elemento_juego(textura: str, ancho: int, alto: int, pos_x: int, pos_y: int) -> dict:
    """
    Crea un botón o cuadro con textura y rectángulo de colisión.

    Args:
        textura (str): Ruta a la imagen.
        ancho (int): Ancho del elemento.
        alto (int): Alto del elemento.
        pos_x (int): Posición X.
        pos_y (int): Posición Y.

    Returns:
        dict: Elemento del juego con 'superficie' y 'rectangulo'.
    """
    superficie = pygame.transform.scale(pygame.image.load(textura), (ancho, alto))
    rectangulo = superficie.get_rect(x=pos_x, y=pos_y)
    return {"superficie": superficie, "rectangulo": rectangulo}

def limpiar_superficie(elemento_juego: dict, textura: str, ancho: int, alto: int) -> None:
    """
    Restaura la textura original del elemento.

    Args:
        elemento_juego (dict): Elemento a limpiar.
        textura (str): Ruta a la imagen.
        ancho (int): Ancho de la superficie.
        alto (int): Alto de la superficie.
    """
    elemento_juego["superficie"] = pygame.transform.scale(pygame.image.load(textura), (ancho, alto))

def obtener_respuesta_click(lista_respuestas: list, pos_click: tuple) -> int | None:
    """
    Devuelve la respuesta seleccionada según el clic.

    Args:
        lista_respuestas (list): Lista de botones de respuesta.
        pos_click (tuple): Posición del clic.

    Returns:
        int | None: Número de respuesta (1-4) o None si no hizo clic en ninguna.
    """
    for i, respuesta in enumerate(lista_respuestas):
        if respuesta["rectangulo"].collidepoint(pos_click):
            return i + 1
    return None

def cambiar_pregunta(lista_preguntas: list, indice: int, caja_pregunta: dict, lista_respuestas: list) -> dict:
    """
    Cambia a la siguiente pregunta y limpia las superficies de respuesta.

    Args:
        lista_preguntas (list): Lista de preguntas.
        indice (int): Índice de la pregunta actual.
        caja_pregunta (dict): Elemento gráfico para la pregunta.
        lista_respuestas (list): Lista de elementos de respuesta.

    Returns:
        dict: Pregunta actual.
    """
    pregunta_actual = lista_preguntas[indice]
    limpiar_superficie(caja_pregunta, "./modules/assets/images/textura_pregunta.png", ANCHO_PREGUNTA, ALTO_PREGUNTA)
    for boton in lista_respuestas:
        limpiar_superficie(boton, "./modules/assets/images/textura_respuesta.png", ANCHO_BOTON, ALTO_BOTON)
    return pregunta_actual

def crear_botones_menu() -> list:
    """
    Crea los botones del menú principal centrados.

    Returns:
        list: Lista de botones con sus superficies y rectángulos.
    """
    lista_botones = []
    cantidad_botones = 4
    espaciado = 20
    alto_total = cantidad_botones * ALTO_BOTON_MENU + (cantidad_botones - 1) * espaciado
    pos_y = (ALTO - alto_total) // 2
    pos_x = (ANCHO - ANCHO_BOTON_MENU) // 2

    for _ in range(cantidad_botones):
        boton = crear_elemento_juego("./modules/assets/images/fondo_menu.png", ANCHO_BOTON_MENU, ALTO_BOTON_MENU, pos_x, pos_y)
        lista_botones.append(boton)
        pos_y += ALTO_BOTON_MENU + espaciado

    return lista_botones

def crear_respuestas(textura: str, ancho: int, alto: int, pos_x: int, pos_y: int, cantidad_respuestas: int) -> list:
    """
    Crea una lista de botones de respuesta verticales.

    Args:
        textura (str): Ruta a la imagen.
        ancho (int): Ancho del botón.
        alto (int): Alto del botón.
        pos_x (int): Posición X inicial.
        pos_y (int): Posición Y inicial.
        cantidad_respuestas (int): Número de respuestas a crear.

    Returns:
        list: Lista de elementos de respuesta.
    """
    lista_respuestas = []
    for _ in range(cantidad_respuestas):
        boton = crear_elemento_juego(textura, ancho, alto, pos_x, pos_y)
        lista_respuestas.append(boton)
        pos_y += 80
    return lista_respuestas

def manejar_texto(cuadro_texto: dict, tecla_presionada: str, bloc_mayus: int, datos_juego: dict) -> None:
    """
    Gestiona la entrada de texto del jugador para el nombre.

    Args:
        cuadro_texto (dict): Elemento gráfico del cuadro.
        tecla_presionada (str): Tecla presionada.
        bloc_mayus (int): Estado del bloqueo de mayúsculas.
        datos_juego (dict): Diccionario de datos del juego.
    """
    nombre_actual = datos_juego["nombre"]

    if tecla_presionada == "backspace" and nombre_actual:
        datos_juego["nombre"] = nombre_actual[:-1]
        limpiar_superficie(cuadro_texto, "./modules/assets/images/textura_respuesta.png", ANCHO_CUADRO, ALTO_CUADRO)

    elif len(tecla_presionada) == 1 and tecla_presionada.isalpha():
        if len(nombre_actual) < 12:
            CLICK_SONIDO.play()
            if bloc_mayus == 8192 or bloc_mayus & pygame.KMOD_SHIFT:
                datos_juego["nombre"] += tecla_presionada.upper()
            else:
                datos_juego["nombre"] += tecla_presionada.lower()