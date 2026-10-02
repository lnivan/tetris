import pygame
import random
import time
from pygame import display

from pygame.event import event_name

pygame.init()
'''
pygame.mixer.music.load('tetris.mp3')
pygame.mixer.music.play(-1)
'''
gray = (100, 100, 100) 
black = (0, 0, 0)

tiempo_entre_bajadas = 1000
grosor_lineas = 1
tamano_cuadros = 4
ancho_juego = 10
largo_juego = 20
puntuacion = 0



coordenada_esquina_pieza = []
coordenadas_pieza = []
posicion_pieza = 1
pieza_actual = 0

screen = pygame.display.set_mode([ancho_juego * tamano_cuadros * 2, largo_juego * tamano_cuadros ])
array_juego = []
for y in range(largo_juego):
    array_juego.append([])
    for x in range(ancho_juego):
        array_juego[y].append(0)

class Pieza:
    def __init__(self, array_pieza):

        self.posicion_uno = []
        self.posicion_dos = []
        self.posicion_tres = []
        self.posicion_cuatro = []
        for x in range(len(array_pieza)):
            self.posicion_uno.append([])
            for y in range(len(array_pieza)):
                self.posicion_uno[x].append(array_pieza[x][y])

        def girar_array_cuadrado(array_entra):
            array_sale = []
            for x in range(len(array_entra)):
                array_sale.append([])
                for y in range(len(array_entra)):
                    array_sale[x].append(0)
            x_reves = len(array_entra)
            y_reves = len(array_entra[0])
            for x in range(len(array_entra)):
                x_reves = x_reves - 1
                y_reves = len(array_entra[0])
                for y in range(len(array_entra)):
                    y_reves = y_reves -1
                    array_sale[y][x_reves] = array_entra[x][y]
            return(array_sale)

        self.posicion_dos = girar_array_cuadrado(self.posicion_uno)

        self.posicion_tres = girar_array_cuadrado(self.posicion_dos)

        self.posicion_cuatro = girar_array_cuadrado(self.posicion_tres)
        
        print(self.posicion_uno)
        print(self.posicion_dos)
        print(self.posicion_tres)
        print(self.posicion_cuatro)



pieza_l = Pieza([[0,0,0,0,0],
                 [0,0,1,0,0],
                 [0,0,1,0,0],
                 [0,0,1,1,0],
                 [0,0,0,0,0]])

pieza_l_reves = Pieza([[0,0,0,0,0],
                       [0,0,2,0,0],
                       [0,0,2,0,0],
                       [0,2,2,0,0],
                       [0,0,0,0,0]])

pieza_rayo = Pieza([[0,0,0,0,0],
                    [0,0,3,0,0],
                    [0,0,3,3,0],
                    [0,0,0,3,0],
                    [0,0,0,0,0]])

pieza_rayo_reves = Pieza([[0,0,0,0,0],
                          [0,0,4,0,0],
                          [0,4,4,0,0],
                          [0,4,0,0,0],
                          [0,0,0,0,0]])

pieza_t = Pieza([[0,0,0,0,0],
                 [0,0,0,0,0],
                 [0,5,5,5,0],
                 [0,0,5,0,0],
                 [0,0,0,0,0]])

pieza_cuadrado = Pieza([[0,0,0,0,0],
                        [0,0,6,6,0],
                        [0,0,6,6,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0]])

pieza_palo = Pieza([[0,0,0,0,0],
                    [0,0,7,0,0],
                    [0,0,7,0,0],
                    [0,0,7,0,0],
                    [0,0,7,0,0]])

def cuadricula_pantalla():
    for i in range(largo_juego + 1):    
        pygame.draw.line(screen, black, (0, tamano_cuadros * i), (ancho_juego * tamano_cuadros, tamano_cuadros * i), grosor_lineas)
    for i in range(ancho_juego + 1):   
        pygame.draw.line(screen, black, (tamano_cuadros * i, 0), (tamano_cuadros * i, largo_juego * tamano_cuadros), grosor_lineas)

def pintar_pieza(pieza,x,y):
    for yy in range(len(pieza)):
        for xx in range(len(pieza[0])):
            if pieza[yy][xx] != 0:
                array_juego[y + yy][x + xx] = pieza[yy][xx]

def pintar_cuadrado(x,y,color):
    pygame.draw.rect(screen,color,pygame.Rect(x * tamano_cuadros,y * tamano_cuadros,tamano_cuadros,tamano_cuadros))

def pintar_cuadrados():

    for y in range(len(array_juego)):
        for x in range(len(array_juego[0])):
            if array_juego[y][x] != 0:
                if array_juego[y][x] == 1:
                    pintar_cuadrado(x,y,(255,128,0))
                elif array_juego[y][x] == 2:
                    pintar_cuadrado(x,y,(0,0,255))
                elif array_juego[y][x] == 3:
                    pintar_cuadrado(x,y,(0,255,0))
                elif array_juego[y][x] == 4:
                    pintar_cuadrado(x,y,(255,0,0))
                elif array_juego[y][x] == 5:
                    pintar_cuadrado(x,y,(153,0,153))
                elif array_juego[y][x] == 6:
                    pintar_cuadrado(x,y,(255,255,0))
                elif array_juego[y][x] == 7:
                    pintar_cuadrado(x,y,(0,255,255))

nueva_pieza_creada = False

def comprobar_filas():
    global puntuacion
    for y in range(len(array_juego)):
        n_de_ceros = 0
        for x in range(len(array_juego[y])):
            if array_juego[y][x] == 0:
                n_de_ceros += 1
        if n_de_ceros == 0:
            array_juego.pop(y)
            array_juego.insert(0,[0,0,0,0,0,0,0,0,0,0])
            int(puntuacion)
            puntuacion = puntuacion + 100

def nueva_pieza():
    global nueva_pieza_creada
    global coordenadas_pieza
    nueva_pieza_creada = True
    global pieza_actual
    global coordenada_esquina_pieza
    global posicion_pieza
    pieza_actual = random.choice([pieza_l,pieza_l_reves,pieza_rayo,pieza_rayo_reves,pieza_t,pieza_cuadrado,pieza_palo])
    coordenada_esquina_pieza = [2,0]
    coordenadas_pieza = []
    comprobar_filas()


def actualizar_posicion_pieza():
    global coordenadas_pieza
    global posicion_pieza
    global nueva_pieza_creada

    for i in range(len(coordenadas_pieza)):
        array_juego[coordenadas_pieza[i][1]][coordenadas_pieza[i][0]] = 0
    coordenadas_pieza = []
    global coordenada_esquina_pieza
    if posicion_pieza == 1:
        print(posicion_pieza)
        pintar_pieza(pieza_actual.posicion_uno,coordenada_esquina_pieza[0],coordenada_esquina_pieza[1])

        coordenadas_anadidas = 0
        for y in range(len(pieza_actual.posicion_uno)):
            for x in range(len(pieza_actual.posicion_uno[0])):
                if pieza_actual.posicion_uno[y][x] != 0:
                    coordenadas_pieza.append([])
                    coordenadas_pieza[coordenadas_anadidas].append(coordenada_esquina_pieza[0] + x)
                    coordenadas_pieza[coordenadas_anadidas].append(coordenada_esquina_pieza[1] + y)
                    coordenadas_anadidas += 1

    if posicion_pieza == 2:
        print(posicion_pieza)
        pintar_pieza(pieza_actual.posicion_dos,coordenada_esquina_pieza[0],coordenada_esquina_pieza[1])

        coordenadas_anadidas = 0
        for y in range(len(pieza_actual.posicion_dos)):
            for x in range(len(pieza_actual.posicion_dos[0])):
                if pieza_actual.posicion_dos[y][x] != 0:
                    coordenadas_pieza.append([])
                    coordenadas_pieza[coordenadas_anadidas].append(coordenada_esquina_pieza[0] + x)
                    coordenadas_pieza[coordenadas_anadidas].append(coordenada_esquina_pieza[1] + y)
                    coordenadas_anadidas += 1

    if posicion_pieza == 3:
        print(posicion_pieza)
        pintar_pieza(pieza_actual.posicion_tres,coordenada_esquina_pieza[0],coordenada_esquina_pieza[1])

        coordenadas_anadidas = 0
        for y in range(len(pieza_actual.posicion_tres)):
            for x in range(len(pieza_actual.posicion_tres[0])):
                if pieza_actual.posicion_tres[y][x] != 0:
                    coordenadas_pieza.append([])
                    coordenadas_pieza[coordenadas_anadidas].append(coordenada_esquina_pieza[0] + x)
                    coordenadas_pieza[coordenadas_anadidas].append(coordenada_esquina_pieza[1] + y)
                    coordenadas_anadidas += 1

    if posicion_pieza == 4:
        print(posicion_pieza)
        pintar_pieza(pieza_actual.posicion_cuatro,coordenada_esquina_pieza[0],coordenada_esquina_pieza[1])

        coordenadas_anadidas = 0
        for y in range(len(pieza_actual.posicion_cuatro)):
            for x in range(len(pieza_actual.posicion_cuatro[0])):
                if pieza_actual.posicion_cuatro[y][x] != 0:
                    coordenadas_pieza.append([])
                    coordenadas_pieza[coordenadas_anadidas].append(coordenada_esquina_pieza[0] + x)
                    coordenadas_pieza[coordenadas_anadidas].append(coordenada_esquina_pieza[1] + y)
                    coordenadas_anadidas += 1

#    for i in range(len(coordenadas_pieza)):
 #       coordenadas_y_baja = []
  #      for a in range(len(coordenadas_pieza)):
   #         if coordenadas_pieza[i][1] > coordenadas_pieza[a][1] and coordenadas_pieza[i][0] == coordenadas_pieza[1][0]:
    #            coordenadas_y_baja.append(coordenadas_pieza[i])

#def bajar_pieza():
 #   for i in range(len(coordenadas_pieza)):
  #      if array_juego[coordenadas_pieza[i][1] + 1][coordenadas_pieza[i][0]] != 0:
   #         for a in coordenadas_pieza:
    #            if a == coordenadas_pieza[i]:
     #               print("hola")
                   
def bajar_piez():
    coordenadas_y_baja = []
    for i in range(len(coordenadas_pieza)):
        coordenadas_y_baja.append([])
    for i in range(len(coordenadas_pieza)):
        for a in range(len(coordenadas_pieza)):
            if coordenadas_pieza[i][1] > coordenadas_pieza[a][1] and coordenadas_pieza[i][0] == coordenadas_pieza[a][0]:
                coordenadas_y_baja[i] = coordenadas_pieza[i]
    numero_de_ceros = 0
    for i in coordenadas_y_baja:
        if i == []:
            numero_de_ceros += 1
    for i in range(numero_de_ceros):
        coordenadas_y_baja.remove([])
    for i in coordenadas_y_baja:
        if array_juego[i[1] + 1][i[0]] != 0 or i[1] == 18:
            nueva_pieza()
            return()
    coordenada_esquina_pieza[1] = coordenada_esquina_pieza[1] + 1


def bajar_pieza():
    global puntuacion
    actualizar_posicion_pieza()
    for i in coordenadas_pieza:
        coordenada_comprobada = []
        coordenada_comprobada.append(i[0])
        coordenada_comprobada.append(i[1] + 1)
        if i[1] == 19:
            nueva_pieza()
            int(puntuacion)
            puntuacion = puntuacion + 10
            return()
        if not(coordenada_comprobada in coordenadas_pieza) and array_juego[coordenada_comprobada[1]][coordenada_comprobada[0]] != 0:
            nueva_pieza()
            int(puntuacion)
            puntuacion = puntuacion + 10
            return()
    coordenada_esquina_pieza[1] = coordenada_esquina_pieza[1] + 1

veces_repeticion = 0

pygame.display.set_caption('Show Text')
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render(str(puntuacion), True, black, gray)
textRect = text.get_rect()
textRect.center = (15 * tamano_cuadros, 3.5 * tamano_cuadros)

def juego():
    global text
    global veces_repeticion
    screen.fill(gray)
    pintar_cuadrados()
    cuadricula_pantalla()
    actualizar_posicion_pieza()
    bajar_pieza()
    #pintar_pieza(pieza_actual, coordenada_esquina_pieza[0], coordenada_esquina_pieza[1])
    display.flip()

def juego2():
    global text
    global veces_repeticion
    screen.fill(gray)
    pintar_cuadrados()
    cuadricula_pantalla()
    actualizar_posicion_pieza()
    #pintar_pieza(pieza_actual, coordenada_esquina_pieza[0], coordenada_esquina_pieza[1])
    display.flip()

nueva_pieza()
tiempo = 0

running = True
while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                coordenada_esquina_pieza[0] = coordenada_esquina_pieza[0] + 1
            if event.key == pygame.K_a:
                coordenada_esquina_pieza[0] = coordenada_esquina_pieza[0] - 1
            if event.key == pygame.K_RIGHT:
                posicion_pieza = posicion_pieza + 1
                if posicion_pieza > 4:
                    posicion_pieza = 1
            if event.key == pygame.K_LEFT:
                posicion_pieza = posicion_pieza - 1
                if posicion_pieza < 1:
                    posicion_pieza = 4
            if event.key == pygame.K_DOWN:
                bajar_pieza()

    tiempo = tiempo + 1
    if tiempo == tiempo_entre_bajadas:
        tiempo = 0
        juego()
    else:
        juego2()
    