# coding: UTF-8
from constants import *
from random import random
from entities import Entity
from centered_figure import CenteredFigure


class PowerUp(Entity):
    def __init__(self, surface, color=None,
                 level=None, sounds=None):

        self.platforms = level.get_platforms()
        self.width = PU_SIDE
        self.height = PU_SIDE
        self.set_center()

        self.y_vel = 0
        if color == COLOR_RED:
            self.effect = "atk-up"
        elif color == COLOR_GREEN:
            self.effect = "heal"
        elif color == COLOR_BLUE:
            self.effect = "range-up"

        self.sounds = sounds
        self.figure = CenteredFigure(
            [(-self.width / 2, self.height / 2),
             (self.width / 2, self.height / 2),
             (self.width / 2, -self.height / 2),
             (-self.width / 2, -self.height / 2)], self.center, color,
            pygame_surface=surface)

    def set_center(self):
        done = False
        while(not done):
            self.center = [random() * SW, random() * SH]
            done = True
            for platform in self.platforms:
                if(
                    platform.intersects(self)
                ):
                    done = False
