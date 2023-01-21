import pathlib
import pygame

BASE_DIR = pathlib.Path(__file__).parent

TEXTURES = {
    'machine': pygame.image.load(BASE_DIR / "assets" / "graphics" / "slot-machine.png"),
    'arrow': pygame.image.load(BASE_DIR / "assets" / "graphics" / "up_arrow.png")
}

pygame.font.init()

FONTS = {
    'large': pygame.font.Font(BASE_DIR / "assets" / "fonts" / "PressStart2P.ttf", 64),
    'short': pygame.font.Font(BASE_DIR / "assets" / "fonts" / "PressStart2P.ttf", 10)
}

MACHINE_WIDTH, MACHINE_HEIGHT = TEXTURES['machine'].get_size()

WINDOW_WIDTH = 150 + MACHINE_WIDTH * 2
WINDOWS_HEIGHT = 200 + MACHINE_HEIGHT

TEXT = "Two-Armed Bandit - By: Abe & Alfredo"
TOTAL = "Total:"