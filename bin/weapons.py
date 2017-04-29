# coding: UTF-8
from centered_figure import CenteredFigure
from constants import *


# clase para manejar ataques y su duración
class Attack(object):
    def __init__(self, player=None, direction=None):
        self.active = False
        self.recoil = False
        self.ticks = 0
        self.direction = direction
        self.player = player

    def tick(self):
        if self.active and self.ticks < self.player.swing:
            self.ticks += 1
        elif self.active and self.ticks == self.player.swing:
            self.active = False
            self.recoil = True
            self.ticks -= 1
        elif self.recoil and self.ticks > 0:
            self.ticks -= 1
        elif self.recoil and self.ticks == 0:
            self.recoil = False

    def is_active(self):
        return self.active

    def is_recoiling(self):
        return self.recoil

    def can_attack(self):
        return not (self.active or self.recoil)

    def set_direction(self, direction):
        self.direction = direction

    def get_direction(self, direction):
        return self.direction

    def start_attack(self, direction):
        self.active = True
        self.direction = direction

    def sword_stop(self):
        return False


# clase que representa una espada
class Sword(object):
    def __init__(self, player):
        self.width = SWORD_WIDTH
        self.height = SWORD_HEIGHT
        self.color = COLOR_RED
        self.x_offset = (self.width + player.width)/2
        self.y_offset = (self.width + player.height)/2
        self.center = player.center
        self.center_backup = [player.center[0], player.center[1]]
        self.figure = CenteredFigure(
            [(-self.width / 2, self.height / 2),
             (self.width / 2, 0),
             (-self.width / 2, -self.height / 2)], self.center, self.color,
             pygame_surface=player.figure.get_surface())
        self.figure_backup = self.figure
        self.atk_inst = Attack(player)

        self.damage = SWORD_DAMAGE

    def draw(self):
        if self.is_attacking:
            self.set_orientation(self.atk_inst.direction)
        self.figure.draw()

    def attack(self, direction):
        self.atk_inst.start_attack(direction)

    def can_attack(self):
        return self.atk_inst.can_attack()

    def is_attacking(self):
        return self.atk_inst.is_active() or self.atk_inst.is_recoiling()

    def set_orientation(self, orientation):
        if orientation == "right":
            self.center[0] += self.x_offset
        elif orientation == "up":
            self.figure.rotate(90)
            self.center[1] -= self.y_offset
        elif orientation == "left":
            self.figure.rotate(180)
            self.center[0] -= self.x_offset
        elif orientation == "down":
            self.figure.rotate(-90)
            self.center[1] += self.y_offset

    def reset_orientation(self):
        self.center = self.center_backup
        self.figure = self.figure_backup

    def tick(self):
        self.atk_inst.tick()
