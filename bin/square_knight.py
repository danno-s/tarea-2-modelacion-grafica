# coding: UTF-8
# imports
import pygame
import os
from pygame.locals import *
from constants import *
from entities import *
from sounds import Sounds
from level import Level

# inicializaciones
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = "1"

# creación de pantalla
surface = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Square Knight")

# carga de assets
sound = Sounds()
level = Level(surface, COLOR_BROWN)

# carga de modelos
player = Player(surface, sounds=sound, level=level)

# reloj del juego
clock = pygame.time.Clock()

counter = 0

# loop principal
while True:

    print(counter)
    counter += 1
    
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
