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

        self.platforms = [Platform(SH - 340, SH - 320, 250, 425),
                          Platform(SH - 340, SH - 320, SW - 425, SW - 250),
                          Platform(SH - 100, SH, -100, SW + 100, "floor"),
                          Platform(-10, 0, 0, SW, "cieling")]

    def draw(self):
        # dibuja en pantalla el nivel
        for plat_index, platform in enumerate(self.platforms):
            poly(self._surface, self.color,
                 [(platform.left, platform.top),
                  (platform.right, platform.top),
                  (platform.right, platform.bottom),
                  (platform.left, platform.bottom)])

    def get_platforms(self):
        # retorna lista con las plataformas en el nivel
        return self.platforms
