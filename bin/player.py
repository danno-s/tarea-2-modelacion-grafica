#coding: UTF-8
# clase que define al jugador
from centered_figure import CenteredFigure
from constants import *


class Player(object):
    def __init__(self, surface, center=[SW / 2, SH / 2], color=COLOR_GREY,
                 sounds=None, level=None):
        self.center = center
        self.hp = 3
        self.height = 50
        self.width = 30
        self.figure = CenteredFigure(
            [(-self.width / 2, self.height / 2),
             (self.width / 2, self.height / 2),
             (self.width / 2, -self.height / 2),
             (-self.width / 2, -self.height / 2)], center, color,
            pygame_surface=surface)
        self._sounds = sounds
        self.ground_height = level.get_ground_height()
        self.platforms = level.get_platforms()

    def draw(self):
        # dibuja al jugador en pantalla
        self.figure.draw()

    def fall(self):
        # hace que el jugador caiga por la gravedad, con una implementación
        # rudimentaria de colisión
        for plat_index, platform in enumerate(self.platforms):
            # si esta sobre o bajo plataforma
            if (
                self.center[0] >= platform[2] and
                self.center[0] <= platform[3]
            ):
                if self.center[1] <= platform[0]:
                    self.center[1] = min(self.center[1] + GRAVITY,
                                         platform[0] - self.height / 2)
                else:
                    self.center[1] = min(self.center[1] + GRAVITY,
                                         self.ground_height - self.height / 2)
            else:
                self.center[1] = min(self.center[1] + GRAVITY,
                                     self.ground_height - self.height / 2)

    def move_right(self):
        for plat_index, platform in enumerate(self.platforms):
            # se salta las plataformas a la izquierda pues el movimiento no es
            # en esa dirección
            if self.center[0] >= platform[2]:
                continue

            if (
                self.center[1] >= platform[0] - self.height / 2 and
                self.center[1] <= platform[1] + self.height / 2
            ):
                self.center[0] = min(self.center[0] + SPEED, platform[2] -
                                     self.width / 2)
                return
            else:
                break

        self.center[0] = min(self.center[0] + SPEED, SW - self.width / 2)

        print self.center[0]

    def move_left(self):
        for plat_index, platform in enumerate(reversed(self.platforms)):
            # se salta las plataformas a la derecha pues el movimiento no es
            # en esa dirección
            if self.center[0] <= platform[2]:
                continue

            if (
                self.center[1] >= platform[0] - self.height / 2 and
                self.center[1] <= platform[1] + self.height / 2
            ):
                self.center[0] = max(self.center[0] - SPEED, platform[2] +
                                     self.width / 2)
                return
            else:
                break

        self.center[0] = max(self.center[0] - SPEED, 0 + self.width / 2)

        print self.center[0]

    def jump(self):
        