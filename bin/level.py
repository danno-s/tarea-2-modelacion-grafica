# coding: UTF-8
# Clase definiendo la estructura del nivel
from pygame.draw import polygon as poly
from constants import *


class Level(object):
    def __init__(self, surface):
        self._surface = surface
        self.ground_height = SH - 150

        # plataformas se describen con listas que contienen las coordenadas de
        # cada plataforma en el nivel, ordenadas de izquierda a derecha, con las
        # coordenadas de cada plataforma ordenadas como corresponde:
        # platforms[i][0] := arriba
        # platforms[i][1] := abajo
        # platforms[i][2] := izquierda
        # platforms[i][3] := derecha

        self.platforms = [[SH - 360, SH - 340, 125, 300],
                          [SH - 360, SH - 340, SW - 300, SW - 125,]]

    def draw(self):
        # dibuja piso
        poly(self._surface, COLOR_BROWN,
             [(0, self.ground_height), (SW, self.ground_height),
              (SW, SH), (0, SH)])

        # dibuja plataformas
        for plat_index, platform in enumerate(self.platforms):
            poly(self._surface, COLOR_BROWN,
                 [(platform[2], platform[0]),
                  (platform[3], platform[0]),
                  (platform[3], platform[1]),
                  (platform[2], platform[1])])

    # funciones que retornan los límites de las plataformas y el suelo
    def get_ground_height(self):
        return self.ground_height

    def get_platforms(self):
        return self.platforms
