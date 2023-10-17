# ourhelp
proyecto de programacion II. queremos pasar el año
import pygame, random, sys, time
from pygame.locals import *

ANCHOVENTANA = 1200
ALTOVENTANA = 640
FPS = 40
TAMANOMAXBOLA = 25
VELOCIDADMAXBOLA = 8
TASANUEVOBOLA = 6
TASAMOVIMIENTOJUGADOR = 5

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

# Establece un pygame, la ventana y el cursor del ratón
pygame.init()
relojPrincipal = pygame.time.Clock()
superficieVentana = pygame.display.set_mode((ANCHOVENTANA, ALTOVENTANA))
pygame.display.set_caption('our help')

# Carga la imagen de fondo
fondo = pygame.image.load('fondo_juego.png')
fondo = pygame.transform.scale(fondo, (ANCHOVENTANA, ALTOVENTANA))

# Establece la imagen de la nave (princesa)
playerImage = pygame.image.load('princesa.png')
rectanguloJugador = playerImage.get_rect()
rectanguloJugador.centerx = ANCHOVENTANA / 2
rectanguloJugador.centery = ALTOVENTANA / 2

# Carga la imagen de la bola de fuego (personaliza la ruta a tu imagen)
bolaImage = pygame.image.load('fuego.png')
bolaImage = pygame.transform.scale(bolaImage, (TAMANOMAXBOLA, TAMANOMAXBOLA))

puntajeMax = 0
tiempoSobrevivido = 0
inicioTiempo = 0
recordTiempo = 0

while True:
    bolasDeFuego = []
    puntaje = 0
    moverArriba = moverAbajo = moverIzquierda = moverDerecha = False
    contadorAgregarBola = 0

    inicioTiempo = time.time()  # Reinicia el tiempo al inicio del juego

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

        for bola in bolasDeFuego:
            superficieVentana.blit(bola['surface'], bola['rect'])

        font = pygame.font.Font(None, 36)
        tiempoTexto = font.render('Tiempo: ' + str(tiempoSobrevivido) + 's', True, (255, 255, 255))
        superficieVentana.blit(tiempoTexto, (10, 10))

        if tiempoSobrevivido > recordTiempo:
            recordTiempo = tiempoSobrevivido

        recordTexto = font.render('Récord: ' + str(recordTiempo) + 's', True, (255, 255, 255))
        superficieVentana.blit(recordTexto, (10, 50))

        pygame.display.update()

        if any(bola['rect'].colliderect(rectanguloJugador) for bola in bolasDeFuego):
            if tiempoSobrevivido > recordTiempo:
                recordTiempo = tiempoSobrevivido
            break

        relojPrincipal.tick(FPS)

    esperarTeclaJugador()