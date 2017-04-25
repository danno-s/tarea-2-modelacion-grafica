# coding: UTF-8
# Handler para los sonidos del juego
from constants import *
import pygame.mixer as mixer


class Sounds(object):
    def __init__(self):
        self._jump = mixer.Sound(SOUND_JUMP)
        self._damage = mixer.Sound(SOUND_DAMAGE)
        self._hit = mixer.Sound(SOUND_HIT)

    def jump(self):
        # reproduce el sonido de un salto
        self._jump.play(0)

    def hit(self):
        # reproduce el sonido de un golpe a enemigo
        self._hit.play(0)

    def damage(self):
        # reproduce el sonido de un golpe al jugador
        self._damage.play(0)