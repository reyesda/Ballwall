import pygame
# import time
import numpy as np
import Hand_Tracking_fuctions as Htf

# iniciar pygame
pygame.init()

# Colores
rojo = (250, 0, 0)
gris = (90, 90, 90)
blanco = (255, 255, 255)

# para abrir el carchivo en modo lectura
with open("puntaje_alto.txt", "r") as puntaje_f:
    hiest = puntaje_f.readline()
    hiest = int(hiest)

# Establecer pantalla
screen_width, screen_height = 400, 700
flags = pygame.NOFRAME
screen_game = pygame.display.set_mode((screen_width, screen_height))
# screen_game = pygame.display.set_mode((screen_width, screen_height), flags=flags)

# formato de los textos
score_font = pygame.font.SysFont('ubuntu', 25)
message_font = pygame.font.SysFont('ubuntu', 30)

clock = pygame.time.Clock()


# funcion para crear un array con 1 y 0 que diga como colocar los bloques
def crear_bloque(size_array):
    blanco_minimo = 4
    # blanco_maximo = int(size_array / 2)
    lleno_maximo = int(size_array / 2)
    bloques = []
    final = []
    total_bloques = 0
    inicial = bool(np.random.randint(0, 2))

    while total_bloques < size_array:
        if inicial:
            bloques.append([inicial, np.random.randint(4, lleno_maximo)])
            inicial = not inicial
        else:
            bloques.append([inicial, np.random.randint(blanco_minimo, blanco_minimo + 1)])
            inicial = not inicial

        total_bloques = 0
        for i in bloques:
            total_bloques += sum(i)

    for i in bloques:
        for j in range(i[1]):
            final.append(i[0])

    if len(final) > size_array:
        while len(final) > size_array:
            final.pop()

    if len(final) < size_array:
        while len(final) < size_array:
            final.append(final[-1])

    return final


# detecta si el jugador toco un bloque
def toco(bloques, jugador):

    puntos_jugador = [[int(jugador.x) - int(jugador.tamano), jugador.y],
                      [int(jugador.x), jugador.y - int(jugador.tamano)],
                      [int(jugador.x) + int(jugador.tamano), jugador.y]]

    for punto_bloque in bloques.contacto:
        for punto_jugador in puntos_jugador:
            if punto_jugador[0] in range(punto_bloque, punto_bloque + bloques.size_cuadro + 1) and\
                    punto_jugador[1] in range(int(bloques.y), int(bloques.y + bloques.size_cuadro) + 1):
                return True

    return False


def print_score(score):
    text = score_font.render("Score: " + str(score), True, blanco)
    screen_game.blit(text, [0, 0])


class obstacles:
    def __init__(self):
        self.color = blanco
        self.velocidad = 0.06
        self.size_array = 20
        self.size_cuadro = 20
        self.y = 0
        self.cuadros = crear_bloque(self.size_array)
        self.velocidad = 0.06
        self.muerte = False
        self.puntos_v = True
        self.contacto = []

    def dibujar(self):
        for i in range(self.size_array):
            if self.cuadros[i]:
                pygame.draw.rect(screen_game, blanco,
                                 (i * self.size_cuadro, round(self.y), self.size_cuadro, self.size_cuadro))
                self.contacto.append(i * self.size_cuadro)

    def bajar(self):
        self.y += self.velocidad

        if self.y >= screen_height - self.size_cuadro:
            self.y = screen_height - self.size_cuadro
            self.muerte = True


# jugador
class ball:
    def __init__(self):
        self.color = rojo
        self.x = screen_width / 2
        self.y = int(screen_height - (screen_height / 5))
        self.tamano = 10
        self.velocidad = 0.08
        self.puntos = 0

    def dibujar_personaje(self):

        if self.x >= screen_width - self.tamano:
            self.x = screen_width - self.tamano

        if self.x <= self.tamano:
            self.x = self.tamano

        pygame.draw.circle(screen_game, self.color, (round(self.x), round(self.y)), self.tamano)

    def mover_derecha(self):
        self.x += self.velocidad

        if self.x >= screen_width - self.tamano:
            self.x = screen_width - self.tamano

    def mover_izquierda(self):
        self.x -= self.velocidad

        if self.x <= self.tamano:
            self.x = self.tamano

    def punto_mas(self, puntos_v):
        if puntos_v:
            self.puntos += 1


def main():
    # se pone el global para editar bariable global dentro de la funcion
    global hiest
    game_over = False
    game_close = False

    jugador = ball()
    # muro puede almacenar varios objetos
    muro = [obstacles()]

    moverI = False
    moverD = False

    clock.tick(30)

    mano = Htf.hands_traking(True, angulo=20)
    px_anterior = 0
    px_siguiente = 0
    diferencias = 0

    while not game_over:

        while game_close:
            # Actualizar pantalla
            # pantalla de game over
            screen_game.fill(gris)
            game_over_mesage = message_font.render("Game Over", True, rojo)
            screen_game.blit(game_over_mesage, [screen_width / 3, screen_height / 3])

            game_over_mesage = message_font.render("Hiest score: " + str(hiest), True, rojo)
            screen_game.blit(game_over_mesage, [screen_width / 3.5, screen_height / 2.6])
            print_score(jugador.puntos)
            pygame.display.update()

            # detecta si se preciona una tecla
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                    continue

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        game_over = True
                        game_close = False
                        continue

                    if event.key == pygame.K_SPACE:
                        main()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_over = True
                game_close = False
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                    continue

                if event.key == pygame.K_LEFT:
                    moverI = True
                    moverD = False
                if event.key == pygame.K_RIGHT:
                    moverD = True
                    moverI = False

        # if moverD:
        #     jugador.mover_derecha()
        # elif moverI:
        #     jugador.mover_izquierda()

        moverD = False
        moverI = False

        if mano.actived():

            jugador.x -= mano.diferencias_neta * 450

        # Actualizar pantalla
        screen_game.fill(gris)

        if moverI or moverD:
            for i in muro:
                i.bajar()

            if toco(muro[0], jugador):
                game_close = True
                if jugador.puntos > hiest:
                    hiest = jugador.puntos
                    # escribe en el archivo el puntaje maximo
                    with open("puntaje_alto.txt", "w") as puntaje_a:
                        puntaje_a.write(str(hiest))

        for i in muro:
            if int(i.y) == int(screen_height * (1.5/5)):
                i.y += 1
                # crea un nuevo objeto dentro de muro para tener varios muros en pantalla
                # este muro se activa cuando el primer muro pasa un punto en la pantalla
                muro.append(obstacles())

        jugador.dibujar_personaje()

        for i in muro:
            i.contacto = []
            # recorre todos los objetos de muro y les puede modificar sus atributos o llamar metodos
            i.dibujar()

        if muro[0].muerte:
            muro.pop(0)

        if jugador.y + jugador.tamano == int(muro[0].y) and muro[0].puntos_v:
            jugador.punto_mas(muro[0].puntos_v)
            muro[0].puntos_v = False
        print_score(jugador.puntos)

        pygame.display.update()
        # time.sleep(2)

    # Cerrar pantalla
    pygame.quit()
    quit()


main()
