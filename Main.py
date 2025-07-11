import pygame 
from modules.Constantes import *
from modules.Menu import *
from modules.Juego import *
from modules.Configuracion import *
from modules.Rankings import *
from modules.Terminado import *

pygame.init()
pygame.display.set_caption("PREGUNTADOS")
icono = pygame.image.load("./modules/assets/images/icono.png")
pygame.display.set_icon(icono)
pantalla = pygame.display.set_mode(PANTALLA)

corriendo = True
reloj = pygame.time.Clock()
bandera_musica = False
ventana_actual = "menu"

#Ustedes la van a cargar del json
lista_rankings = []

while corriendo:
    reloj.tick(FPS)
    cola_eventos = pygame.event.get()
    
    if ventana_actual == "menu":
        if bandera_musica == True:
            pygame.mixer.music.stop()
            bandera_musica = False
        reiniciar_estadisticas(datos_juego)
        ventana_actual = mostrar_menu(pantalla,cola_eventos)
    elif ventana_actual == "juego":
        porcentaje_volumen = datos_juego["volumen_musica"] / 100
        
        if bandera_musica == False:
            pygame.mixer.music.load("./modules/assets/sounds/musica.mp3")
            pygame.mixer.music.set_volume(porcentaje_volumen)
            pygame.mixer.music.play(-1)
            bandera_musica = True
            
        ventana_actual = mostrar_juego(pantalla,cola_eventos,datos_juego)
    elif ventana_actual == "salir":
        corriendo = False
    elif ventana_actual == "ajustes":
        ventana_actual = mostrar_ajustes(pantalla,cola_eventos,datos_juego)
    elif ventana_actual == "rankings":
        ventana_actual = mostrar_rankings(pantalla,cola_eventos,lista_rankings)
    elif ventana_actual == "terminado":
        ventana_actual = mostrar_fin_juego(pantalla,cola_eventos,datos_juego,lista_rankings)

    # print(ventana_actual)
    pygame.display.flip()

pygame.quit()
    
    