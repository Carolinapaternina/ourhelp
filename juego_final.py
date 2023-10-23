import pygame, random, sys, time
from pygame.locals import *

ANCHOVENTANA = 1200
ALTOVENTANA = 640
FPS = 120
TAMANOMAXBOLA = 50
VELOCIDADMAXBOLA = 8
TASANUEVOBOLA = 6
TASAMOVIMIENTOJUGADOR = 2
COLORTEXTO = (255, 255, 255)

def terminar():
    pygame.quit()
    sys.exit()

def esperarTeclaJugador():
    while True:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                terminar()
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    terminar()
                return

def dibujarTexto(texto, font, superficie, x, y):
    objetotexto = font.render(texto, 1, COLORTEXTO)
    rectangulotexto = objetotexto.get_rect()
    rectangulotexto.topleft = (x, y)
    superficie.blit(objetotexto, rectangulotexto)

pygame.init()
pygame.mixer.init()

font = pygame.font.SysFont(None, 48)

pygame.mixer.music.load('musica_fondo.mp3')  

relojPrincipal = pygame.time.Clock()
superficieVentana = pygame.display.set_mode((ANCHOVENTANA, ALTOVENTANA))
pygame.display.set_caption('our help')

fondo = pygame.image.load('fondo_juego_ciudad.png')
fondo = pygame.transform.scale(fondo, (ANCHOVENTANA, ALTOVENTANA))

playerImage = pygame.image.load('princesa.png')
rectanguloJugador = playerImage.get_rect()
rectanguloJugador.centerx = ANCHOVENTANA / 2
rectanguloJugador.centery = ALTOVENTANA / 1.05
bolaImage = pygame.image.load('fuego.png')
bolaImage = pygame.transform.scale(bolaImage, (TAMANOMAXBOLA, TAMANOMAXBOLA))

nuevoPersonajeImage = pygame.image.load('principe.png')
rectanguloprincipe = nuevoPersonajeImage.get_rect()
rectanguloprincipe.centerx = ANCHOVENTANA / 2
rectanguloprincipe.centery = ALTOVENTANA / 12

dibujarTexto('Our Help - El Libertador IED', font, superficieVentana, (ANCHOVENTANA / 3.1), (ALTOVENTANA / 3))
dibujarTexto('Presione una tecla para comenzar el juego', font, superficieVentana, (ANCHOVENTANA / 4), (ALTOVENTANA / 2.5))
dibujarTexto('si duras 30,60 o 100 segundos puedes llegar ha ganar algo :)', font, superficieVentana, (ANCHOVENTANA / 8), (ALTOVENTANA / 2.1))
dibujarTexto('Buena suerte', font, superficieVentana, (ANCHOVENTANA / 2.5), (ALTOVENTANA / 1.8))

pygame.display.update()
esperarTeclaJugador()

DURACION_MAXIMA = 100
TIEMPO_APARICION_DULCES = [30, 60, 100]
CANTIDADES_DULCES = [1, 3, 5]
mostrarMensaje = False
recordTiempo = 0

while True:
    bolasDeFuego = []
    puntaje = 0
    moverArriba = moverAbajo = moverIzquierda = moverDerecha = False
    contadorAgregarBola = 0
    inicioTiempo = time.time()

    pygame.mixer.music.play(-1, 0.0)

    while True:
        puntaje += 1
        tiempoSobrevivido = int(time.time() - inicioTiempo)

        for evento in pygame.event.get():
            if evento.type == QUIT:
                terminar()

            if evento.type == KEYDOWN:
                if evento.key == K_UP:
                    moverArriba = True
                elif evento.key == K_DOWN:
                    moverAbajo = True
                elif evento.key == K_LEFT:
                    moverIzquierda = True
                elif evento.key == K_RIGHT:
                    moverDerecha = True

            if evento.type == KEYUP:
                if evento.key == K_ESCAPE:
                    terminar()
                if evento.key == K_UP:
                    moverArriba = False
                elif evento.key == K_DOWN:
                    moverAbajo = False
                elif evento.key == K_LEFT:
                    moverIzquierda = False
                elif evento.key == K_RIGHT:
                    moverDerecha = False

        contadorAgregarBola += 1
        if contadorAgregarBola == TASANUEVOBOLA:
            contadorAgregarBola = 0
            bolaSize = TAMANOMAXBOLA
            newBola = {'rect': pygame.Rect(random.randint(0, ANCHOVENTANA - bolaSize), 0 - bolaSize, bolaSize, bolaSize),
                       'speed': random.randint(VELOCIDADMAXBOLA // 2, VELOCIDADMAXBOLA),
                       'surface': bolaImage,
                       }
            bolasDeFuego.append(newBola)

        if moverArriba and rectanguloJugador.top > 0:
            rectanguloJugador.move_ip(0, -TASAMOVIMIENTOJUGADOR)
        if moverAbajo and rectanguloJugador.bottom < ALTOVENTANA:
            rectanguloJugador.move_ip(0, TASAMOVIMIENTOJUGADOR)
        if moverIzquierda and rectanguloJugador.left > 0:
            rectanguloJugador.move_ip(-TASAMOVIMIENTOJUGADOR, 0)
        if moverDerecha and rectanguloJugador.right < ANCHOVENTANA:
            rectanguloJugador.move_ip(TASAMOVIMIENTOJUGADOR, 0)

        for bola in bolasDeFuego:
            bola['rect'].move_ip(0, bola['speed'])

        bolasDeFuego = [bola for bola in bolasDeFuego if bola['rect'].top <= ALTOVENTANA]

        superficieVentana.blit(fondo, (0, 0))
        superficieVentana.blit(playerImage, rectanguloJugador)
        superficieVentana.blit(nuevoPersonajeImage, rectanguloprincipe)

        for bola in bolasDeFuego:
            superficieVentana.blit(bola['surface'], bola['rect'])

        font = pygame.font.Font(None, 36)
        tiempoTexto = font.render('Tiempo: ' + str(tiempoSobrevivido) + 's', True, (255, 255, 255))
        superficieVentana.blit(tiempoTexto, (10, 10))

        if tiempoSobrevivido > recordTiempo:
            recordTiempo = tiempoSobrevivido

        recordTexto = font.render('Récord: ' + str(recordTiempo) + 's', True, (255, 255, 255))
        superficieVentana.blit(recordTexto, (10, 50))

        # Mostrar mensajes de dulces de forma intermitente
        for index, tiempo_aparicion in enumerate(TIEMPO_APARICION_DULCES):
            if tiempoSobrevivido == tiempo_aparicion and tiempoSobrevivido % 5 == 0:
                mensaje = f'¡Ganaste {CANTIDADES_DULCES[index]} dulces!'
                dibujarTexto(mensaje, font, superficieVentana, (ANCHOVENTANA / 2) - 100, (ALTOVENTANA / 2) + 50)
                mostrarMensaje = True
            else:
                mostrarMensaje = False

        pygame.display.update()

        if any(bola['rect'].colliderect(rectanguloJugador) for bola in bolasDeFuego):
            if tiempoSobrevivido > recordTiempo:
                recordTiempo = tiempoSobrevivido
            break

        if rectanguloJugador.colliderect(rectanguloprincipe):
            mensaje = '¡Ganaste!'
            dibujarTexto(mensaje, font, superficieVentana, (ANCHOVENTANA / 1.5), (ALTOVENTANA / 3.9))
            pygame.display.update()
            pygame.time.wait(1000)  # Espera 2 segundos antes de salir del juego
            break

        relojPrincipal.tick(FPS)

    rectanguloJugador.centerx = ANCHOVENTANA / 2
    rectanguloJugador.centery = ALTOVENTANA / 1.05
    rectanguloprincipe.centerx = ANCHOVENTANA / 2
    rectanguloprincipe.centery = ALTOVENTANA / 12

    # Reiniciar la lista de bolas de fuego
    bolasDeFuego = []

    pygame.mixer.music.stop()

    dibujarTexto('Juego Terminado', font, superficieVentana, (ANCHOVENTANA / 6), (ALTOVENTANA / 3.9))
    dibujarTexto('Presione una tecla para repetir.', font, superficieVentana, (ANCHOVENTANA / 6) , (ALTOVENTANA / 3.3))
    pygame.display.update()

    esperarTeclaJugador()