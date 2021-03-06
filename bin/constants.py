# coding: UTF-8
# Definicion de constantes para el programa

# Tamaño de pantalla

SW = 1280
SH = 720

# Colores

COLOR_BLACK = (0, 0, 0)
COLOR_SKY = (175, 255, 247)
COLOR_BROWN = (130, 110, 32)
COLOR_GREY = (128, 128, 128)
COLOR_RED = (160, 28, 28)
COLOR_PINK = (255, 107, 230)
COLOR_GREEN = (107, 255, 124)
COLOR_BLUE = (13, 77, 181)
COLOR_WHITE = (255, 255, 255)

# Rutas a los archivos

SOUND_JUMP = "sound/jump.wav"
SOUND_DAMAGE = "sound/damage.wav"
SOUND_HIT = "sound/hit.wav"
SOUND_ATK = "sound/attack.wav"
FONT = "fonts/VCR_OSD_MONO.ttf"

# FPS

FPS = 60

# variables del juego

GRAVITY = 0.5
JUMP_SPEED = -18.0

# jugador

PLAYER_HEIGHT = 80
PLAYER_WIDTH = 48
PLAYER_WALK_SPEED = 5.2
PLAYER_HP = 7
PLAYER_SWING_SPEED = 7
PLAYER_I_FRAMES = 50
SWORD_HEIGHT = 20
SWORD_WIDTH = 80
SWORD_DAMAGE = 1

# enemigo

ENEMY_HEIGHT = 50
ENEMY_WIDTH = 30
ENEMY_WALK_SPEED = 2.7
ENEMY_HP = 5
ENEMY_DAMAGE = 1
ENEMY_I_FRAMES = 15
ENEMY_LIMIT = 1

# powerups

PU_SIDE = 20
PU_COLORS = [COLOR_GREEN, COLOR_RED, COLOR_BLUE]

# probabilidades

ENEMY_PROB = 1
POWER_UP_PROB = 0.1

# HEAL_PROB + ATK_PORB + RANGE_PROB = 100
HEAL_PROB = 50
ATK_PROB = 30
RANGE_PROB = 20
