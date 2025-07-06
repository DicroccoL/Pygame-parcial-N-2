import comodines
from comodines import comodines_usados, puntaje_doble, doble_chance_activada, pasar_activado
import pygame
from Constantes import *
from Preguntas import *
from Funciones import *

pygame.init()

pygame.display.set_caption("PREGUNTADOS")
icono = pygame.image.load("icono.png")
pygame.display.set_icon(icono)

pantalla = pygame.display.set_mode(PANTALLA)
datos_juego = {"puntuacion":0,"vidas":CANTIDAD_VIDAS,"nombre":"","tiempo_restante":30}
fondo_pantalla = pygame.transform.scale(pygame.image.load("fondo.jpg"), PANTALLA)

#Elemento del juego
caja_pregunta = crear_elemento_juego("textura_pregunta.png",ANCHO_PREGUNTA,ALTO_PREGUNTA,80,80)
lista_respuestas = crear_respuestas("textura_respuesta.png",ANCHO_BOTON,ALTO_BOTON,125,245,3)

# Variables para manejar el comodín bomba
opciones_bomba = None
bomba_activada = False

mezclar_lista(lista_preguntas)

corriendo = True
reloj = pygame.time.Clock()
evento_tiempo = pygame.USEREVENT
pygame.time.set_timer(evento_tiempo,1000)

def mostrar_juego(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    global opciones_bomba, bomba_activada
    
    if "racha" not in datos_juego:
        datos_juego["racha"] = 0
    if "mensaje_vida" not in datos_juego:
        datos_juego["mensaje_vida"] = {"mostrar": False, "contador": 0}
    if "doble_chance_usado" not in datos_juego:
        datos_juego["doble_chance_usado"] = False

    retorno = "juego"
    
    pregunta_actual = lista_preguntas[datos_juego['indice']]
    
    if datos_juego["vidas"] == 0 or datos_juego["tiempo_restante"] == 0:
        retorno = "terminado"
    
    for evento in cola_eventos:
        if evento.type == evento_tiempo:
            datos_juego["tiempo_restante"] -= 1
            
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                # Primero verificar comodines
                comodin_clickeado = comodines.detectar_click_comodin(evento.pos)
                if comodin_clickeado and not comodines.comodines_usados[comodin_clickeado]:
                    # Manejar clic en comodín
                    comodines.comodines_usados[comodin_clickeado] = True
                    if comodin_clickeado == "bomba":
                        opciones = [pregunta_actual["respuesta_1"], pregunta_actual["respuesta_2"], pregunta_actual["respuesta_3"]]
                        opciones_bomba = comodines.aplicar_comodin("bomba", opciones, pregunta_actual["respuesta_correcta"])
                        bomba_activada = True
                    elif comodin_clickeado == "x2":
                        comodines.aplicar_comodin("x2", None, None)
                    elif comodin_clickeado == "doble_chance":
                        comodines.aplicar_comodin("doble_chance", None, None)
                    elif comodin_clickeado == "pasar":
                        comodines.aplicar_comodin("pasar", None, None)
                        datos_juego['indice'] += 1
                        if datos_juego['indice'] == len(lista_preguntas):
                            mezclar_lista(lista_preguntas)
                            datos_juego['indice'] = 0
                        pregunta_actual = cambiar_pregunta(lista_preguntas,datos_juego['indice'],caja_pregunta,lista_respuestas)
                        # Resetear efectos de bomba
                        bomba_activada = False
                        opciones_bomba = None
                        datos_juego["doble_chance_usado"] = False
                
                # Si no fue clic en comodín, verificar respuestas
                if not comodin_clickeado:
                    respuesta = obtener_respuesta_click(lista_respuestas,evento.pos)
                    if respuesta != None:
                        # Verificar que el índice de respuesta sea válido (0, 1, 2)
                        if respuesta < 0 or respuesta > 2:
                            continue
                        
                        # Obtener el texto de la respuesta clickeada
                        respuesta_texto = pregunta_actual[f"respuesta_{respuesta + 1}"]
                            
                        # Verificar si la bomba está activada y la respuesta no está en las opciones válidas
                        if bomba_activada and opciones_bomba:
                            # La bomba elimina 2 opciones incorrectas, solo permite tocar la correcta y una incorrecta
                            if respuesta_texto not in opciones_bomba:
                                # Respuesta eliminada por bomba, no hacer nada
                                continue
                        
                        # Manejar doble chance ANTES de verificar respuesta
                        if comodines.doble_chance_activada and not datos_juego["doble_chance_usado"]:
                            # Primera oportunidad con doble chance
                            respuesta_correcta = verificar_respuesta(datos_juego, pregunta_actual, respuesta)
                            if respuesta_correcta:
                                CLICK_SONIDO.play()
                                # Aplicar puntos dobles si está activado
                                if comodines.puntaje_doble:
                                    datos_juego["puntuacion"] += 100
                                
                                # Resetear efectos temporales
                                comodines.resetear_efectos_temporales()
                                comodines.doble_chance_activada = False
                                datos_juego["doble_chance_usado"] = False
                            else:
                                # Primera respuesta incorrecta con doble chance - restaurar puntos
                                datos_juego["puntuacion"] += 25  # Compensar la resta que hizo verificar_respuesta
                                datos_juego["doble_chance_usado"] = True
                                ERROR_SONIDO.play()
                                # NO avanzar a la siguiente pregunta
                                continue
                        else:
                            # Respuesta normal o segunda oportunidad de doble chance
                            respuesta_correcta = verificar_respuesta(datos_juego,pregunta_actual,respuesta)
                            
                            if respuesta_correcta:
                                CLICK_SONIDO.play()
                                # Aplicar puntos dobles si está activado
                                if comodines.puntaje_doble:
                                    # La función verificar_respuesta ya agregó 100 puntos
                                    # Agregamos 100 puntos adicionales para hacer el total 200
                                    datos_juego["puntuacion"] += 100
                                
                                # Resetear efectos temporales
                                comodines.resetear_efectos_temporales()
                                datos_juego["doble_chance_usado"] = False
                            else:
                                # Respuesta incorrecta normal o segunda oportunidad fallida
                                ERROR_SONIDO.play()
                                if comodines.doble_chance_activada:
                                    # Se agotó la segunda oportunidad
                                    comodines.doble_chance_activada = False
                                    datos_juego["doble_chance_usado"] = False
                        
                        # Avanzar a la siguiente pregunta
                        datos_juego['indice'] += 1
                        if datos_juego['indice'] == len(lista_preguntas):
                            mezclar_lista(lista_preguntas)
                            datos_juego['indice'] = 0
                        pregunta_actual = cambiar_pregunta(lista_preguntas,datos_juego['indice'],caja_pregunta,lista_respuestas)
                        
                        # Resetear efectos de bomba
                        bomba_activada = False
                        opciones_bomba = None
                        datos_juego["doble_chance_usado"] = False

    pantalla.blit(fondo_pantalla,(0,0))
    # Dibujar menú de comodines
    comodines.dibujar_comodines(pantalla, FUENTE_COMODIN)
    pantalla.blit(caja_pregunta["superficie"],caja_pregunta["rectangulo"])
    
    for i in range(len(lista_respuestas)):
        pantalla.blit(lista_respuestas[i]["superficie"],lista_respuestas[i]["rectangulo"])

    mostrar_texto(caja_pregunta["superficie"],pregunta_actual["pregunta"],(20,40),FUENTE_PREGUNTA,COLOR_NEGRO)
    
    # Mostrar respuestas (algunas pueden estar ocultas por bomba)
    for i in range(min(3, len(lista_respuestas))):  # Asegurar que solo procesamos 3 respuestas
        respuesta_key = f"respuesta_{i + 1}"
        if respuesta_key in pregunta_actual:
            respuesta_texto = pregunta_actual[respuesta_key]
            if not bomba_activada or not opciones_bomba or respuesta_texto in opciones_bomba:
                mostrar_texto(lista_respuestas[i]["superficie"],respuesta_texto,(20,20),FUENTE_RESPUESTA,COLOR_BLANCO)
            else:
                # Respuesta eliminada por bomba
                mostrar_texto(lista_respuestas[i]["superficie"],"[ELIMINADA]",(20,20),FUENTE_RESPUESTA,COLOR_ROJO)
    
    mostrar_texto(pantalla,f"VIDAS: {datos_juego['vidas']}",(10,10),FUENTE_TEXTO)
    mostrar_texto(pantalla,f"PUNTUACION: {datos_juego['puntuacion']}",(10,40),FUENTE_TEXTO)
    mostrar_texto(pantalla,f"TIEMPO: {datos_juego['tiempo_restante']} s",(300,10),FUENTE_TEXTO)
    
    # Mostrar estado de comodines activos
    if comodines.puntaje_doble:
        mostrar_texto(pantalla, "¡PUNTOS x2 ACTIVO!", (120, 420), FUENTE_RESPUESTA, COLOR_VERDE)
    if comodines.doble_chance_activada:
        mostrar_texto(pantalla, "¡DOBLE CHANCE ACTIVO!", (120, 440), FUENTE_RESPUESTA, COLOR_AZUL)
    
    if datos_juego["mensaje_vida"]["mostrar"]:
        mostrar_texto(pantalla, "¡Vida extra por racha!", (120, 450), FUENTE_RESPUESTA, COLOR_VERDE)
        datos_juego["mensaje_vida"]["contador"] -= 1
        if datos_juego["mensaje_vida"]["contador"] <= 0:
            datos_juego["mensaje_vida"]["mostrar"] = False
    return retorno