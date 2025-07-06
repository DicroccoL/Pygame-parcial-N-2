import pygame
from Constantes import *
from Funciones import *
import json
from datetime import datetime

pygame.init()
cuadro_texto = crear_elemento_juego("textura_respuesta.png",ANCHO_CUADRO,ALTO_CUADRO,140,140)
fondo = pygame.transform.scale(pygame.image.load("game over.png"), PANTALLA)
boton_volver = crear_elemento_juego("textura_respuesta.png", 100, 40, 10, 10)
boton_guardar = crear_elemento_juego("textura_respuesta.png", 100, 40, 400, 10)



def mostrar_fin_juego(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict,lista_rankings:list) -> str:
    retorno = "terminado"
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1 and boton_volver["rectangulo"].collidepoint(evento.pos):
                CLICK_SONIDO.play()
                datos_juego["guardado"] = False
                datos_juego["guardado_exito"] = False
                datos_juego["nombre"] = ""
                retorno = "menu"

            elif evento.button == 1 and boton_guardar["rectangulo"].collidepoint(evento.pos):
                entrada = {
                            "nombre": datos_juego["nombre"],
                            "puntuacion": datos_juego["puntuacion"],
                            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }

                try:
                    with open("partidas.json", "r", encoding="utf-8") as f:
                         partidas = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                        partidas = []

                partidas.append(entrada)

                with open("partidas.json", "w", encoding="utf-8") as f:
                    json.dump(partidas, f, indent=4, ensure_ascii=False)
                        
                datos_juego["guardado"] = True
                datos_juego["guardado_exito"] = True

        elif evento.type == pygame.KEYDOWN:
            tecla_presionada = pygame.key.name(evento.key)    
            bloc_mayus = pygame.key.get_mods()
            
            manejar_texto(cuadro_texto,tecla_presionada,bloc_mayus,datos_juego)   
    
    #Metanle un fondo de pantalla al game over
    pantalla.blit(fondo, (0, 0))

    pantalla.blit(cuadro_texto["superficie"],cuadro_texto["rectangulo"])
    mostrar_texto(pantalla,f"Usted obtuvo: {datos_juego["puntuacion"]} puntos",(130,100),FUENTE_TEXTO,COLOR_BLANCO)
    pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])
    mostrar_texto(boton_volver["superficie"], "MENU", (5, 5), FUENTE_RESPUESTA, COLOR_BLANCO)
    pantalla.blit(boton_guardar["superficie"], boton_guardar["rectangulo"])
    mostrar_texto(boton_guardar["superficie"], "GUARDAR", (5, 5), FUENTE_RESPUESTA, COLOR_BLANCO)
    if datos_juego.get("guardado_exito"):
        mostrar_texto(pantalla, "¡Guardado!", (250, 160), FUENTE_RESPUESTA, COLOR_BLANCO)

    limpiar_superficie(cuadro_texto, "textura_respuesta.png", ANCHO_CUADRO, ALTO_CUADRO)

    if datos_juego["nombre"] != "":
        if random.randint(1, 2) == 1:
            mostrar_texto(cuadro_texto["superficie"], f"{datos_juego['nombre']}|", (10, 5), FUENTE_CUADRO_TEXTO, COLOR_BLANCO)
        else:
            mostrar_texto(cuadro_texto["superficie"], f"{datos_juego['nombre']}", (10, 5), FUENTE_CUADRO_TEXTO, COLOR_BLANCO)
    else:
        mostrar_texto(cuadro_texto["superficie"], "INGRESE SU NOMBRE", (10, 15), FUENTE_RESPUESTA, "#736767")



    return retorno 
