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
from powerups import PowerUp


# inicializaciones
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = "1"

# creación de pantalla
surface = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Square Knight")

# carga de assets
sound = Sounds()
level = Level(surface, COLOR_BROWN)
font = pygame.font.Font('fonts/VCR_OSD_MONO.ttf', 40)
big_font = pygame.font.Font('fonts/VCR_OSD_MONO.ttf', 80)


# carga de modelos
player = Player(surface, sounds=sound, level=level)
enemies = []
powerups = []

# reloj del juego
clock = pygame.time.Clock()

counter = 0
enemy_prob = 1
power_up_prob = 0.1
score = 0
state = "main_menu"

# loop principal
while True:

    # setea reloj
    clock.tick(FPS)

    # salida
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    if state == "main_menu":
        title_text = big_font.render("Square Knight", 1, COLOR_WHITE)
        begin_text = font.render("Aprieta espacio para comenzar", 1,
                                 COLOR_WHITE)
        surface.fill(COLOR_BLACK)
        surface.blit(title_text, (375, 300))
        surface.blit(begin_text, (575, 650))

        keys = pygame.key.get_pressed()

        if keys[K_SPACE]:
            state = "playing"

    if state == "playing":
        if random() * 100 < enemy_prob and len(enemies) < 5:
            enemies += [Enemy(surface, sounds=sound, level=level,
                        player=player)]
            enemy_prob = 1

        if random() * 100 < power_up_prob:
            r = random() * 100
            if r < 50:
                color_index = 0
            elif r < 80:
                color_index = 1
            else:
                color_index = 2
            powerups += [PowerUp(surface, level=level,
                                 color=PU_COLORS[color_index])]

        # eventos
        keys = pygame.key.get_pressed()

        if keys[K_RIGHT]:
            player.move_right()

        if keys[K_LEFT]:
            player.move_left()

        if keys[K_z] and player.on_ground():
            player.jump(JUMP_SPEED)

        if not player.is_attacking() and keys[K_x] and pygame.KEYDOWN:
            if keys[K_UP]:
                player.attack("up")
            elif keys[K_DOWN] and not player.on_ground():
                player.attack("down")
            elif keys[K_RIGHT]:
                player.attack("right")
            elif keys[K_LEFT]:
                player.attack("left")
            else:
                player.attack(player.get_last_move())

        # actualiza modelos
        player.update_y()
        player.tick()
        for enemy in enemies:
            enemy.update()
            enemy.update_y()

        # checkea colisiones entre entidades
        for enemy in enemies:
            if enemy.is_hit():
                enemy.recieve_damage()
                enemy.get_i_frames()
                if player.sword.get_atk_direction() == "down":
                    player.jump(JUMP_SPEED/2.0)

            if enemy.get_hp() <= 0:
                enemies.remove(enemy)
                score += 100

            if enemy.hit_player():
                player.recieve_damage()
                player.get_i_frames()
                score = max(score-50, 0)

        for powerup in powerups:
            if powerup.figure.intersect(player.figure):
                if powerup.effect == "atk-up":
                    player.sword.damage = min(4, player.sword.damage + 0.5)
                    print(player.sword.damage)
                elif powerup.effect == "heal":
                    player.hp += 1
                elif powerup.effect == "range-up":
                    player.sword.scale(1.1)
                powerups.remove(powerup)

        if player.get_hp() <= 0:
            state = "game_over"

        # pinta fondo
        surface.fill(COLOR_SKY)

        # dibuja
        level.draw()
        player.draw()
        for enemy in enemies:
            enemy.draw()
        for powerup in powerups:
            powerup.draw()
        hp_text = font.render("HP: " + str(player.get_hp()), 1, COLOR_BLACK)
        score_text = font.render("SCORE: " + str(score), 1, COLOR_BLACK)

        # voltea a pantalla
        surface.blit(hp_text, (20, 11))
        surface.blit(score_text, (SW - 300, 11))

    elif state == "game_over":
        game_over_text = big_font.render("Game Over!", 1, COLOR_WHITE)
        retry_text = font.render("Aprieta 'r' para jugar de nuevo", 1,
                                 COLOR_WHITE)
        surface.fill(COLOR_BLACK)
        surface.blit(game_over_text, (425, 300))
        surface.blit(retry_text, (525, 650))

        keys = pygame.key.get_pressed()

        if keys[K_r]:
            state = "playing"

    pygame.display.flip()
