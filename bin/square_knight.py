# coding: UTF-8
# imports
import pygame
import os
from pygame.locals import *
from constants import *
from entities import *
from sounds import Sounds
from level import Level
from random import random


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
enemies = []

# reloj del juego
clock = pygame.time.Clock()

counter = 0
randCount = 1

# loop principal
while True:

    # print(counter)
    # counter += 1
    print(str(enemies))

    if random() * 100 < randCount and len(enemies) < 3:
        enemies += [Enemy(surface, sounds=sound, level=level, player=player)]
        randCount = 1

    # setea reloj
    clock.tick(FPS)

    # eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    keys = pygame.key.get_pressed()

    if keys[K_RIGHT]:
        player.move_right()
        player.set_last_move("right")

    if keys[K_LEFT]:
        player.move_left()
        player.set_last_move("left")

    if keys[K_z] and player.on_ground():
        player.jump()

    if not player.is_attacking():
        if keys[K_x] and keys[K_UP]:
            player.attack("up")
        elif keys[K_x] and keys[K_DOWN] and not player.on_ground():
            player.attack("down")
        elif keys[K_x] and keys[K_RIGHT]:
            player.attack("right")
        elif keys[K_x] and keys[K_LEFT]:
            player.attack("left")
        elif keys[K_x]:
            player.attack(player.get_last_move())

    # actualiza modelos
    player.update_y()
    player.tick()
    for enemy in enemies:
        enemy.update()

    # checkea colisiones entre entidades
    for enemy in enemies:
        if enemy.is_hit():
            enemy.recieve_damage()
            enemy.get_i_frames()

        if enemy.get_hp() <= 0:
            enemies.remove(enemy)

        if enemy.hit_player():
            player.recieve_damage()
            player.get_i_frames()

    # pinta fondo
    surface.fill(COLOR_SKY)

    # dibuja
    level.draw()
    player.draw()
    for enemy in enemies:
        enemy.draw()

    # voltea a pantalla
    pygame.display.flip()
