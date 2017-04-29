# coding: UTF-8
# clase que define a la entidad
from centered_figure import CenteredFigure
from constants import *
from sounds import Sounds
from weapons import *


class Entity(object):
    def __init__(self, surface, center=[SW / 2, SH / 2], color=None,
                 level=None, sounds=None, stats=None):

        self.center = center
        self.y_vel = 0
        self.jumped = False

        self.height = stats[0]
        self.width = stats[1]
        self.hp = stats[2]
        self.speed = stats[3]

        self.sounds = sounds
        self.platforms = level.get_platforms()
        self.figure = CenteredFigure(
            [(-self.width / 2, self.height / 2),
             (self.width / 2, self.height / 2),
             (self.width / 2, -self.height / 2),
             (-self.width / 2, -self.height / 2)], center, color,
            pygame_surface=surface)

        self.counter = 0

    def draw(self):
        # dibuja a la entidad en pantalla
        self.figure.draw()

    def update_y(self):
        if self.on_ground() and not self.jumped:
            self.y_vel = 0
        elif self.on_ground() and self.jumped and self.y_vel >= 0:
            self.y_vel = 0
            self.jumped = False
        elif self.on_cieling() and self.jumped and self.y_vel < 0:
            self.y_vel = 0
            self.jumped = False
        else:
            self.y_vel += GRAVITY

        # hace que la entidad caiga por la gravedad, con una implementación
        # rudimentaria de colisión
        for platform in self.platforms:
            if self.y_vel >= 0 and platform.is_below(self):
                self.center[1] = min(self.center[1] + self.y_vel,
                                     platform.top - self.height / 2)
                break
            elif self.y_vel < 0 and platform.is_above(self):
                self.center[1] = max(self.center[1] + self.y_vel,
                                     platform.bottom + self.height / 2)
                break

    def move_right(self):
        if self is Player:
            self.last_move = "right"
        for platform in self.platforms:
            # se salta las plataformas a la izquierda pues el movimiento no es
            # en esa dirección
            if not platform.is_right(self):
                continue

            if platform.is_right(self) and platform.is_beside(self):
                self.center[0] = min(self.center[0] + self.speed,
                                     platform.left - self.width / 2)
                return
            else:
                break
        self.center[0] = min(self.center[0] + self.speed, SW - self.width / 2)

    def move_left(self):
        if self is Player:
            self.last_move = "left"
        for platform in reversed(self.platforms):
            # se salta las plataformas a la derecha pues el movimiento no es
            # en esa dirección
            if not platform.is_left(self):
                continue

            if platform.is_left(self) and platform.is_beside(self):
                self.center[0] = max(self.center[0] - self.speed,
                                     platform.right + self.width / 2)
                return
            else:
                break

        self.center[0] = max(self.center[0] - self.speed, 0 + self.width / 2)

    def jump(self):
        # hace que la entidad salte y reproduzca un sonido
        self.sounds.jump()
        self.y_vel = JUMP_SPEED
        self.jumped = True

    def on_ground(self):
        # verifica si la entidad esta en el piso
        for platform in self.platforms:
            if(
                platform.is_below(self) and
                self.center[1] + self.height / 2 == platform.top
            ):
                return True

        return False

    def on_cieling(self):
        # verifica si la entidad esta en el techo
        for platform in self.platforms:
            if(
                platform.is_above(self) and
                self.center[1] - self.height / 2 == platform.bottom
            ):
                return True

        return False


# entidad controlada por el jugador
class Player(Entity):
    def __init__(self, surface, center=[SW / 2, SH / 2], color=COLOR_GREY,
                 level=None, sounds=None, stats=[PLAYER_HEIGHT,
                 PLAYER_WIDTH, PLAYER_HP, PLAYER_WALK_SPEED,
                 PLAYER_SWING_SPEED]):

        # variables relacionadas con el estado
        self.center = center
        self.y_vel = 0
        self.jumped = False
        self.last_move = "right"

        # variables relacionadas con stats
        self.height = stats[0]
        self.width = stats[1]
        self.hp = stats[2]
        self.speed = stats[3]
        self.swing = stats[4]

        # variables que almacenan propiedades de la entidad
        self.sounds = sounds
        self.platforms = level.get_platforms()
        self.figure = CenteredFigure(
            [(-self.width / 2, self.height / 2),
             (self.width / 2, self.height / 2),
             (self.width / 2, -self.height / 2),
             (-self.width / 2, -self.height / 2)], center, color,
            pygame_surface=surface)
        self.sword = Sword(self)

        self.counter = 0  # debugging purposes

    def attack(self, direction):
        # Sounds.attack()
        self.sword.attack(direction)

    def draw(self):
        # dibuja al jugador y su espada si esta atacando en pantalla
        self.figure.draw()
        if self.is_attacking():
            self.sword.draw()

    def is_attacking(self):
        return self.sword.is_attacking()

    def get_last_move(self):
        return self.last_move

    def tick(self):
        self.sword.tick()


class Enemy(Entity):
    def __init__(self, surface, center=[SW / 2, SH / 2], color=COLOR_GREY,
                 level=None, sounds=None, stats=[ENEMY_HEIGHT,
                 ENEMY_WIDTH, ENEMY_HP, ENEMY_WALK_SPEED]):

        self.center = center
        self.y_vel = 0
        self.jumped = False

        self.height = stats[0]
        self.width = stats[1]
        self.hp = stats[2]
        self.speed = stats[3]

        self.platforms = level.get_platforms()
        self.figure = CenteredFigure(
            [(-self.width / 2, self.height / 2),
             (self.width / 2, self.height / 2),
             (self.width / 2, -self.height / 2),
             (-self.width / 2, -self.height / 2)], center, color,
            pygame_surface=surface)

        self.counter = 0
