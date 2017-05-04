# coding: UTF-8
# clase que define a la entidad
from centered_figure import CenteredFigure
from constants import *
from sounds import Sounds
from weapons import *
from random import random


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

    def jump(self, jumpspeed):
        # hace que la entidad salte y reproduzca un sonido
        self.sounds.jump()
        self.y_vel = jumpspeed
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
        self.i_frames = 0

    def attack(self, direction):
        # Sounds.attack()
        self.sword.attack(direction)

    def draw(self):
        # dibuja al jugador y su espada si esta atacando en pantalla
        self.figure.draw()
        if self.is_attacking():
            self.sword.draw()

    def is_attacking(self):
        return self.sword.is_active() or self.sword.is_recoiling()

    def set_last_move(self, direction):
        self.last_move = direction

    def get_last_move(self):
        return self.last_move

    def recieve_damage(self):
        self.hp -= ENEMY_DAMAGE
        self.sounds.damage()

    def tick(self):
        self.sword.tick()
        if self.i_frames > 0:
            self.i_frames -= 1

    def get_i_frames(self):
        self.i_frames = PLAYER_I_FRAMES

    def has_i_frames(self):
        if self.i_frames > 0:
            return True
        return False

    def get_hp(self):
        return self.hp


class Enemy(Entity):
    def __init__(self, surface, color=COLOR_BLACK,
                 level=None, sounds=None, stats=[ENEMY_HEIGHT,
                 ENEMY_WIDTH, ENEMY_HP, ENEMY_WALK_SPEED],
                 player=None):
        if random() < 0.5:
            self.center = [-50, SH - 125]
        else:
            self.center = [SW + 50, SH - 125]
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
             (-self.width / 2, -self.height / 2)], self.center, color,
            pygame_surface=surface)
        self.player = player
        self.sounds = sounds

        self.counter = 0
        self.i_frames = 0

    def is_left(self, player):
        if self.center[0] + self.width / 2 < player.center[0]:
            return True
        return False

    def is_right(self, player):
        if self.center[0] - self.width / 2 > player.center[0]:
            return True
        return False

    def is_below(self, player):
        if self.center[1] - self.height / 2 > player.center[1] + player.height / 2:
            return True
        return False

    def update(self):
        if not self.has_i_frames():
            if self.is_left(self.player):
                self.move_right()
            elif self.is_right(self.player):
                self.move_left()

        if self.i_frames > 0:
            self.i_frames -= 1

    def is_hit(self):
        if (
            self.figure.intersect(self.player.sword.current_figure) and
            not self.has_i_frames()
        ):
            return True
        return False

    def hit_player(self):
        if (
            self.figure.intersect(self.player.figure) and
            not self.player.has_i_frames()
        ):
            return True
        return False

    def recieve_damage(self):
        self.hp -= self.player.sword.damage
        self.sounds.hit()

    def get_i_frames(self):
        self.i_frames = ENEMY_I_FRAMES

    def has_i_frames(self):
        if self.i_frames > 0:
            return True
        return False

    def get_hp(self):
        return self.hp
