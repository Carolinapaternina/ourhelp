import pygame, random, sys, time
from pygame.locals import *

ANCHOVENTANA = 1200
ALTOVENTANA = 640
FPS = 40
TAMANOMINBOLA = 10
TAMANOMAXBOLA = 25
VELOCIDADMINBOLA = 1
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
                if evento.key == K_ESCAPE: # Sale al presionar ESCAPE
                    terminar()
                return

# Establece un pygame, la ventana y el cursor del ratón
pygame.init()
relojPrincipal = pygame.time.Clock()
superficieVentana = pygame.display.set_mode((ANCHOVENTANA, ALTOVENTANA))
pygame.display.set_caption('Iour help')

# Carga la imagen de fondo
fondo = pygame.image.load('fondo_juego_ciudad.png')
fondo = pygame.transform.scale(fondo, (ANCHOVENTANA, ALTOVENTANA))

# Establece la imagen de la nave (princesa)
playerImage = pygame.image.load('princesa.png')
rectanguloJugador = playerImage.get_rect()
rectanguloJugador.centerx = ANCHOVENTANA / 2
rectanguloJugador.centery = ALTOVENTANA / 2

puntajeMax = 0
tiempoSobrevivido = 0  # Variable para contar el tiempo
inicioTiempo = time.time()  # Guarda el tiempo de inicio del juego
while True:
    # Establece el comienzo del juego
    bolasDeFuego = []
    puntaje = 0
    moverArriba = moverAbajo = moverIzquierda = moverDerecha = False
    contadorAgregarBola = 0

    while True: # El ciclo del juego se mantiene mientras se esté jugando
        puntaje += 1 # Incrementa el puntaje
        tiempoSobrevivido = int(time.time() - inicioTiempo)  # Calcula el tiempo transcurrido

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

        # Añade bolas de fuego en la parte superior de la pantalla, de ser necesarios.
        contadorAgregarBola += 1
        if contadorAgregarBola == TASANUEVOBOLA:
            contadorAgregarBola = 0
            bolaSize = random.randint(TAMANOMINBOLA, TAMANOMAXBOLA)
            newBola = {'rect': pygame.Rect(random.randint(0, ANCHOVENTANA - bolaSize), 0 - bolaSize, bolaSize, bolaSize),
                       'speed': random.randint(VELOCIDADMINBOLA, VELOCIDADMAXBOLA),
                       }
            bolasDeFuego.append(newBola)

        # Mueve el jugador en las cuatro direcciones.
        if moverArriba and rectanguloJugador.top > 0:
            rectanguloJugador.move_ip(0, -TASAMOVIMIENTOJUGADOR)
        if moverAbajo and rectanguloJugador.bottom < ALTOVENTANA:
            rectanguloJugador.move_ip(0, TASAMOVIMIENTOJUGADOR)
        if moverIzquierda and rectanguloJugador.left > 0:
            rectanguloJugador.move_ip(-TASAMOVIMIENTOJUGADOR, 0)
        if moverDerecha and rectanguloJugador.right < ANCHOVENTANA:
            rectanguloJugador.move_ip(TASAMOVIMIENTOJUGADOR, 0)

        # Mueve las bolas de fuego.
        for bola in bolasDeFuego:
            bola['rect'].move_ip(0, bola['speed'])

        # Elimina las bolas de fuego que han caído por debajo.
        bolasDeFuego = [bola for bola in bolasDeFuego if bola['rect'].top <= ALTOVENTANA]

        # Dibuja el mundo del juego en la ventana.
        superficieVentana.blit(fondo, (0, 0))  # Dibuja el fondo
        superficieVentana.blit(playerImage, rectanguloJugador)  # Dibuja la nave

        # Dibuja cada bola de fuego
        for bola in bolasDeFuego:
            pygame.draw.rect(superficieVentana, (255, 0, 0), bola['rect'])

        # Dibuja el contador de tiempo
        font = pygame.font.Font(None, 36)
        tiempoTexto = font.render('Tiempo: ' + str(tiempoSobrevivido) + 's', True, (255, 255, 255))
        superficieVentana.blit(tiempoTexto, (10, 10))

        pygame.display.update()

        # Verifica si alguna bola de fuego impactó en el jugador.
        if any(bola['rect'].colliderect(rectanguloJugador) for bola in bolasDeFuego):
            if puntaje > puntajeMax:
                puntajeMax = puntaje # Establece nuevo puntaje máximo
            break

        relojPrincipal.tick(FPS)

    # Frena el juego y muestra "Juego Terminado"
    esperarTeclaJugador()