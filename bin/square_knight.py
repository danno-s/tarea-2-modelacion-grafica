# coding: UTF-8
# imports
import pygame
import os
from pygame.locals import *
from sounds import Sounds
from constants import *
from level import Level
from player import Player

# inicializaciones
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = "1"

# creación de pantalla
surface = pygame.display.set_mode((SW, SH))

# carga de assets
sound = Sounds()
level = Level(surface)

# carga de modelos
player = Player(surface, sounds=sound, level=level)

# reloj del juego
clock = pygame.time.Clock()

# loop principal
while True:

    # setea reloj
    clock.tick(FPS)

    # eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    keys = pygame.key.get_pressed()

    if keys[K_RIGHT]:
        player.move_right()

    if keys[K_LEFT]:
        player.move_left()

    if keys[K_z] and player.on_ground():
        player.jump()

    # actualiza modelos
    player.update_y()

    # pinta fondo
    surface.fill(COLOR_SKY)

    # dibuja
    level.draw()
    player.draw()

    # voltea a pantalla
    pygame.display.flip()
