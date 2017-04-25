#coding: UTF-8
# clase que define al jugador
from centered_figure import CenteredFigure
from constants import *


class Player(object):
    def __init__(self, surface, center=[SW / 2, SH / 2], color=COLOR_GREY,
                 sounds=None, level=None):
        self.center = center
        self.y_vel = 0
        self.jumped = False
        self.hp = 3
        self.height = 50
        self.width = 30
        self.figure = CenteredFigure(
            [(-self.width / 2, self.height / 2),
             (self.width / 2, self.height / 2),
             (self.width / 2, -self.height / 2),
             (-self.width / 2, -self.height / 2)], center, color,
            pygame_surface=surface)
        self.sounds = sounds
        self.ground_height = level.get_ground_height()
        self.platforms = level.get_platforms()

    def draw(self):
        # dibuja al jugador en pantalla
        self.figure.draw()

    def update_y(self):
        if self.on_ground() and not self.jumped:
            self.y_vel = 0
        elif self.on_ground() and self.jumped and self.y_vel >= 0:
            self.y_vel = 0
            self.jumped = False
        elif self.on_cieling() and self.jumped:
            self.y_vel = 0
            self.jumped = False
        else:
            self.y_vel += GRAVITY

        # hace que el jugador caiga por la gravedad, con una implementación
        # rudimentaria de colisión
        for plat_index, platform in enumerate(self.platforms):
            if (self.y_vel >= 0):  # cayendo
                if (
                    self.center[0] > platform[2] - self.width / 2 and
                    self.center[0] < platform[3] + self.width / 2
                ):
                    if self.center[1] <= platform[1]:
                        self.center[1] = min(self.center[1] + self.y_vel,
                                             platform[0] - self.height / 2)
                        break
                else:
                    self.center[1] = min(self.center[1] + self.y_vel,
                                         self.ground_height - self.height / 2)
                    break
            else:  # subiendo
                if (
                    self.center[0] > platform[2] - self.width / 2 and
                    self.center[0] < platform[3] + self.width / 2
                ):
                    if self.center[1] >= platform[0]:
                        self.center[1] = max(self.center[1] + self.y_vel,
                                             platform[1] + self.height / 2)
                        break
                else:
                    self.center[1] = max(self.center[1] + self.y_vel,
                                         self.height / 2)
                    break

    def move_right(self):
        for plat_index, platform in enumerate(self.platforms):
            # se salta las plataformas a la izquierda pues el movimiento no es
            # en esa dirección
            if self.center[0] >= platform[2]:
                continue

            if (  # si puede colisionar con el lado de una plataforma
                self.center[1] > platform[0] - self.height / 2 and
                self.center[1] < platform[1] + self.height / 2
            ):
                self.center[0] = min(self.center[0] + WALK_SPEED, platform[2] -
                                     self.width / 2)
                return
            else:
                break

        self.center[0] = min(self.center[0] + WALK_SPEED, SW - self.width / 2)

    def move_left(self):
        for plat_index, platform in enumerate(reversed(self.platforms)):
            # se salta las plataformas a la derecha pues el movimiento no es
            # en esa dirección
            if self.center[0] <= platform[3]:
                continue

            if (  # si puede colisionar con el lado de una plataforma
                self.center[1] > platform[0] - self.height / 2 and
                self.center[1] < platform[1] + self.height / 2
            ):
                self.center[0] = max(self.center[0] - WALK_SPEED, platform[3] +
                                     self.width / 2)
                return
            else:
                break

        self.center[0] = max(self.center[0] - WALK_SPEED, 0 + self.width / 2)

    def jump(self):
        self.y_vel = JUMP_SPEED
        self.jumped = True
        self.sounds.jump()

    def on_ground(self):
        for plat_index, platform in enumerate(self.platforms):
            if (
                    self.center[0] > platform[2] - self.width / 2 and
                    self.center[0] < platform[3] + self.width / 2
            ):
                if (self.center[1] >= platform[0] - self.height / 2 and
                   self.center[1] <= platform[1] - self.height / 2):
                    return True
                else:
                    break

        if self.center[1] >= self.ground_height - self.height / 2:
            return True

        return False

    def on_cieling(self):
        for plat_index, platform in enumerate(self.platforms):
            if (
                    self.center[0] > platform[2] - self.width / 2 and
                    self.center[0] < platform[3] + self.width / 2
            ):
                if (self.center[1] >= platform[0] + self.height / 2 and
                   self.center[1] <= platform[1] + self.height / 2):
                    return True
                else:
                    break

        if self.center[1] <= self.height / 2:
            return True

        return False
