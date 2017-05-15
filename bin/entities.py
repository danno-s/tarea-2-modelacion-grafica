# coding: UTF-8
# Clase que define a los jugadores y enemigos
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
        self.last_move = "right"

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
        # calcula donde debiese estar la entidad en el eje y
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
        # procesa el movimiento hacia la derecha, incluyendo colisiones con
        # plataformas
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
        # procesa el movimiento hacia la izquierda, incluyendo colisiones con
        # plataformas
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

    def get_last_move(self):
        return self.last_move


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
        self.i_frames = 0

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

    def attack(self, direction):
        # maneja el ataque del jugador
        self.sounds.attack()
        self.sword.attack(direction)

    def draw(self):
        # dibuja al jugador y su espada si esta atacando en pantalla
        if self.i_frames % 2 == 1:
            return
        self.figure.draw()
        if self.is_attacking():
            self.sword.draw()

    def is_attacking(self):
        # retorna valor booleano sobre el estado de ataque del jugador
        return self.sword.is_active() or self.sword.is_recoiling()

    def recieve_damage(self):
        # actualiza los stats del jugador para que reciba daño
        self.hp -= ENEMY_DAMAGE
        self.sounds.damage()

    def tick(self):
        # actualiza el ataque y estado de invincibilidad del jugador
        self.sword.tick()
        if self.i_frames > 0:
            self.i_frames -= 1

    def get_i_frames(self):
        # le da al jugador una corta invincibilidad
        self.i_frames = PLAYER_I_FRAMES

    def has_i_frames(self):
        # retorna valor booleano sobre el estado de invincibilidad del jugador
        if self.i_frames > 0:
            return True
        return False

    def get_hp(self):
        # retorna puntos de vida del jugador
        return self.hp


class Enemy(Entity):
    def __init__(self, surface, color=COLOR_BLACK,
                 level=None, sounds=None, stats=[ENEMY_HEIGHT,
                 ENEMY_WIDTH, ENEMY_HP, ENEMY_WALK_SPEED],
                 player=None):

        # variables relacionadas con el movimiento
        if random() < 0.5:
            self.center = [-50, SH - 125]
        else:
            self.center = [SW + 50, SH - 125]
        self.y_vel = 0
        self.jumped = False
        self.last_move = "right"

        # variables relacionadas con los stats
        self.height = stats[0]
        self.width = stats[1]
        self.hp = stats[2]
        self.speed = stats[3] + random() - 0.5
        self.i_frames = 0

        # variables relacionadas con el nivel
        self.platforms = level.get_platforms()
        self.figure = CenteredFigure(
            [(-self.width / 2, self.height / 2),
             (self.width / 2, self.height / 2),
             (self.width / 2, -self.height / 2),
             (-self.width / 2, -self.height / 2)], self.center, color,
            pygame_surface=surface)
        self.player = player
        self.sounds = sounds

    def draw(self):
        # dibuja al jugador y su espada si esta atacando en pantalla
        if self.i_frames % 2 == 1:
            return
        self.figure.draw()

    def is_left(self, player):
        # valor booleano que retorna True si el enemigo está a la izquierda del
        # jugador
        if self.center[0] + self.width / 2 < player.center[0]:
            return True
        return False

    def is_right(self, player):
        # valor booleano que retorna True si el enemigo está a la derecha del
        # jugador
        if self.center[0] - self.width / 2 > player.center[0]:
            return True
        return False

    def is_below(self, player):
        # valor booleano que retorna True si el enemigo está bajo el jugador
        if self.center[1] - self.height / 2 > player.center[1] + player.height / 2:
            return True
        return False

    def is_above(self, player):
        # valor booleano que retorna True si el enemigo está sobre el jugador
        if self.center[1] + self.height / 2 < player.center[1] - player.height / 2:
            return True
        return False

    def update(self):
        # función que decide adonde debiese moverse el enemigo para alcanzar al
        # jugador
        if not self.has_i_frames():
            if self.is_below(self.player):
                if abs(self.center[0] - self.player.center[0]) < 126:
                    if self.is_left(self.player):
                        self.move_left()
                    elif self.is_right(self.player):
                        self.move_right()
                elif abs(self.center[0] - self.player.center[0]) > 152:
                    if self.is_left(self.player):
                        self.move_right()
                    elif self.is_right(self.player):
                        self.move_left()
                elif self.on_ground():
                    if random() < 0.2:
                        self.jump(JUMP_SPEED * 0.75)
            elif self.is_above(self.player) and self.on_ground():
                if self.is_left(self.player):
                    self.move_left()
                elif self.is_right(self.player):
                    self.move_right()
            else:
                if self.is_left(self.player):
                    self.move_right()
                elif self.is_right(self.player):
                    self.move_left()
        if self.i_frames > 0:
            self.i_frames -= 1

        self.update_y()

        if self.y_vel != 0:
            self.y_vel -= 0.2

    def is_hit(self):
        # valor booleano que retorna True si el enemigo colisiona con la espada
        # del jugador
        if (
            self.figure.intersect(self.player.sword.current_figure) and
            not self.has_i_frames()
        ):
            return True
        return False

    def hit_player(self):
        # valor booleano que retorna True si el enemigo colisiona con el
        # jugador
        if (
            self.figure.intersect(self.player.figure) and
            not self.player.has_i_frames()
        ):
            return True
        return False

    def recieve_damage(self):
        # actualiza los stats del enemigo para que este reciba daño
        self.hp -= self.player.sword.damage
        self.sounds.hit()

    def get_i_frames(self):
        # le entrega una corta invincibilidad al enemigo
        self.i_frames = ENEMY_I_FRAMES

    def has_i_frames(self):
        # valor booleano que retorna True si el enemigo es invencible
        if self.i_frames > 0:
            return True
        return False

    def get_hp(self):
        # retorna puntos de vida del enemigo
        return self.hp
