import pathlib

import pygame

# Grid
ROWS = 16
COLS = 16

# Size of the square tiles used in this environment.
TILE_SIZE = 33
TILE_SIZE_WALL = 30
NUM_TILES = ROWS * COLS
NUM_ACTIONS = 4
INITIAL_STATE = 0

# Resolution to emulate
VIRTUAL_WIDTH = TILE_SIZE * COLS
VIRTUAL_HEIGHT = TILE_SIZE * ROWS + 30

# Scale factor between virtual screen and window
H_SCALE = 16
V_SCALE = 16

# Resolution of the actual window
WINDOW_WIDTH = TILE_SIZE * H_SCALE 
WINDOW_HEIGHT = TILE_SIZE * H_SCALE

# Default pause time between steps (in seconds)
DEFAULT_DELAY = 0.5

BASE_DIR = pathlib.Path(__file__).parent

# Textures used in the environment
TEXTURES = {
    'metal': pygame.image.load(BASE_DIR / "assets" / "graphics" / "fondo.png"),
    'baterry-lost-point': pygame.image.load(BASE_DIR / "assets" / "graphics" / "battery-lost.png"),
    'explosion': pygame.image.load(BASE_DIR / "assets" / "graphics" / "explosion.png"),
    'baterry-charge': pygame.image.load(BASE_DIR / "assets" / "graphics" / "battery5.png"),
    'battery0-1': pygame.image.load(BASE_DIR / "assets" / "graphics" / "battery0-1.png"),
    'battery0-2': pygame.image.load(BASE_DIR / "assets" / "graphics" / "battery0-2.png"),
    'battery0-3': pygame.image.load(BASE_DIR / "assets" / "graphics" / "battery0-3.png"),
    'battery0-4': pygame.image.load(BASE_DIR / "assets" / "graphics" / "battery0-4.png"),
    'battery0-5': pygame.image.load(BASE_DIR / "assets" / "graphics" / "battery0-5.png"),
    'battery0': pygame.image.load(BASE_DIR / "assets" / "graphics" / "battery0.png"),
    'battery1': pygame.image.load(BASE_DIR / "assets" / "graphics" / "battery1.png"),
    'battery2': pygame.image.load(BASE_DIR / "assets" / "graphics" / "battery2.png"),
    'battery3': pygame.image.load(BASE_DIR / "assets" / "graphics" / "battery3.png"),
    'battery4': pygame.image.load(BASE_DIR / "assets" / "graphics" / "battery4.png"),
    'battery5': pygame.image.load(BASE_DIR / "assets" / "graphics" / "battery5.png"),
    
    'spacecraft': pygame.image.load(BASE_DIR / "assets" / "graphics" / "spacecraft.png"),
    'background': pygame.image.load(BASE_DIR / "assets" / "graphics" / "head.png"),
    'character': [
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "robot-l.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "robot-down.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "robot-r.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "robot-up.png")
    ],
    'character-win': [
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "robot-winr.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "robot-down.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "robot-winl.png")
    ]
}

pygame.font.init()

FONTS = {
    'large': pygame.font.Font(BASE_DIR / "assets" / "fonts" / "Bangers-Regular.ttf", 40),
    'short': pygame.font.Font(BASE_DIR / "assets" / "fonts" / "Bangers-Regular.ttf", 17),
    'short-1': pygame.font.Font(BASE_DIR / "assets" / "fonts" / "Bangers-Regular.ttf", 14)
}

COPY = "Robot Battery - By: Abe & Alfredo"
BATTERY = "Battery:"
STEP = "STEP:"
LOST = "¡LOST GAME!"

# Initializing the mixer
pygame.mixer.init()

# Loading music
pygame.mixer.music.load(BASE_DIR / "assets" / "sounds" / "game.ogg")

# Sound effects
SOUNDS = {
    'game-init': pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "game-init.ogg"),
    'lost-battery': pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "lost-battery.ogg"),
    'lost-game': pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "lost-game.ogg"),
    'win': pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "game-win.ogg")
}

