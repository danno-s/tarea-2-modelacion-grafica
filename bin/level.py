# coding: UTF-8
# Clase definiendo la estructura del nivel
from pygame.draw import polygon as poly
from platform import Platform
from constants import *


class Level(object):
    def __init__(self, surface, color=COLOR_BROWN):
        self._surface = surface

        self.color = color

        # se genera una plataforma para cada plataforma, valga la redundancia,
        # y luego se define una plataforma para el suelo y otra para el techo,
        # para evitar la trivialidad de algunas funciones

        self.platforms = [Platform(SH - 180, SH - 160, 125, 300),
                          Platform(SH - 180, SH - 160, SW - 300, SW - 125),
                          Platform(SH - 150, SH, 0, SW),  # floor
                          Platform(-10, 0, 0, SW)]

    def draw(self):
        for plat_index, platform in enumerate(self.platforms):
            poly(self._surface, self.color,
                 [(platform.left, platform.top),
                  (platform.right, platform.top),
                  (platform.right, platform.bottom),
                  (platform.left, platform.bottom)])

    #  retornn los límites de las plataformas y el suelo
    def get_platforms(self):
        return self.platforms
