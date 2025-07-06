import pygame
import os
from Constantes import *
from Funciones import *

pygame.init()

boton_volver = crear_elemento_juego("textura_respuesta.png",100,40,10,10)
fondo = pygame.transform.scale(pygame.image.load("fondo.jpg"), PANTALLA)

def mostrar_rankings(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],lista_rankings:list) -> str:
    retorno = "rankings"
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    retorno = "menu"
    
    pantalla.fill(COLOR_BLANCO)
    
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])
    import json

    rankings = []
    if os.path.exists("partidas.json"):
        try:
            with open("partidas.json", "r", encoding="utf-8") as f:
                partidas = json.load(f)
                rankings = sorted(partidas, key=lambda x: x["puntuacion"], reverse=True)
        except (FileNotFoundError, json.JSONDecodeError):
            rankings = []

    y = 100
    for entrada in rankings[:10]:
        nombre = entrada.get("nombre", "Sin nombre")
        puntaje = entrada.get("puntuacion", 0)
        fecha = entrada.get("fecha", "")
        mostrar_texto(pantalla, f"{nombre} - {puntaje} pts - {fecha}", (60, y), FUENTE_RESPUESTA, COLOR_NEGRO)
        y += 30


        mostrar_texto(boton_volver["superficie"],"VOLVER",(5,5),FUENTE_RESPUESTA,COLOR_BLANCO)

    return retorno
    