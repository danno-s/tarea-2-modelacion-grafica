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
            self.ticks -= 0.3
        elif self.recoil and self.ticks <= 0:
            self.recoil = False
            self.ticks = 0

    def is_active(self):
        return self.active

    def is_recoiling(self):
        return self.recoil

    def can_attack(self):
        return not (self.active or self.recoil)

    def get_direction(self):
        return self.direction

    def start_attack(self, direction):
        self.active = True
        self.direction = direction

# clase que representa una espada
class Sword(object):
    def __init__(self, player):
        self.width = SWORD_WIDTH
        self.height = SWORD_HEIGHT
        self.color = COLOR_RED
        self.x_offset = (self.width + player.width) / 2
        self.y_offset = (self.width + player.height) / 2
        self.center = player.center
        self.current_figure = None
        self.figure_right = CenteredFigure(
            [(-self.width / 2, self.height / 2),
             (self.width / 2, 0),
             (-self.width / 2, -self.height / 2)], self.center, self.color,
            pygame_surface=player.figure.get_surface())
        self.figure_right.offset([self.x_offset, 0])
        self.figure_up = CenteredFigure(
            [(-self.height / 2, self.width / 2),
             (0, -self.width / 2),
             (self.height / 2, self.width / 2)], self.center, self.color,
            pygame_surface=player.figure.get_surface())
        self.figure_up.offset([0, -self.y_offset])
        self.figure_left = CenteredFigure(
            [(self.width / 2, self.height / 2),
             (self.width / 2, -self.height / 2),
             (-self.width / 2, 0)], self.center, self.color,
            pygame_surface=player.figure.get_surface())
        self.figure_left.offset([-self.x_offset, 0])
        self.figure_down = CenteredFigure(
            [(-self.height / 2, -self.width / 2),
             (self.height / 2, -self.width / 2),
             (0, self.width / 2)], self.center, self.color,
            pygame_surface=player.figure.get_surface())
        self.figure_down.offset([0, self.y_offset])
        self.atk_inst = Attack(player)

        self.damage = SWORD_DAMAGE

    def draw(self):
        if self.is_active() and not self.is_recoiling():
            direction = self.atk_inst.get_direction()
            if direction == "up":
                self.figure_up.draw()
                self.current_figure = self.figure_up
            elif direction == "left":
                self.figure_left.draw()
                self.current_figure = self.figure_left
            elif direction == "down":
                self.figure_down.draw()
                self.current_figure = self.figure_down
            else:
                self.figure_right.draw()
                self.current_figure = self.figure_right
        else:
            self.current_figure = None

    def scale(self, factor):
        self.figure_right.scale(factor)
        self.figure_up.scale(factor)
        self.figure_left.scale(factor)
        self.figure_down.scale(factor)

    def attack(self, direction):
        self.atk_inst.start_attack(direction)

    def can_attack(self):
        return self.atk_inst.can_attack()

    def is_active(self):
        return self.atk_inst.is_active()

    def is_recoiling(self):
        return self.atk_inst.is_recoiling()

    def get_atk_direction(self):
        return self.atk_inst.get_direction()

    def tick(self):
        self.atk_inst.tick()
