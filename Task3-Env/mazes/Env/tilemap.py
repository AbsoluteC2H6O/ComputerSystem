import pygame

from . import settings


class Tile:
    def __init__(self, x, y, texture_name):
        self.x = x
        self.y = y
        self.texture_name = texture_name

    def render(self, surface):
        surface.blit(settings.TEXTURES[self.texture_name], (self.x, self.y))


class TileMap:
    def __init__(self, tile_texture_names, walls,tile_texture_walls):
        self.tiles = []
        self.walls = []
        tile_counter = 0
        for i in range(settings.ROWS):
            for j in range(settings.COLS):
                # if walls[tile_counter]
                # print('walls', walls)
                # print('walls tile_counter', walls[tile_counter])
                self.tiles.append(
                Tile(
                    j * settings.TILE_SIZE,
                    i * settings.TILE_SIZE,
                    tile_texture_names[tile_counter])
                )
                if (tile_texture_walls[tile_counter]):
                    self.walls.append(
                        Tile(
                            j * settings.TILE_SIZE,
                            i * settings.TILE_SIZE,
                           tile_texture_walls[tile_counter])
                    )
             
                tile_counter += 1

    def render(self, surface):
        for tile in self.tiles:
            tile.render(surface)
        for tile in self.walls:
            tile.render(surface)
