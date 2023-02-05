import pygame
from pygame.locals import *
from . import settings
from .tilemap import TileMap
import time

class World:
    def __init__(self, title, state, action):
        pygame.init()
        pygame.display.init()
        pygame.mixer.music.play(loops=-1)
        self.render_surface = pygame.Surface(
            (settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)
        )
        self.screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        )
        pygame.display.set_caption(title)
        self.current_state = state
        self.current_action = action
        self.render_character = True
        self.render_goal = True
        self.tilemap = None
        self.finish_state = None
        self.iteration = 0
        self._create_tilemap()

    def _create_tilemap(self):
        tile_texture_names = ["metal" for _ in range(settings.NUM_TILES)]
        for _, actions_table in settings.P.items():
            for _, possibilities in actions_table.items():
                for _, state, reward, terminated in possibilities:
                    if terminated:
                        if reward > 0:
                            self.finish_state = state
                        else:
                            tile_texture_names[state] = "baterry-lost-point"

        tile_texture_names[self.finish_state] = "metal"
        self.tilemap = TileMap(tile_texture_names)

    def reset(self, state, action):
        self.state = state
        self.action = action
        self.render_character = True
        self.render_goal = True
        for tile in self.tilemap.tiles:
            if tile.texture_name == "explosion":
                tile.texture_name = "baterry-lost-point"

    def update(self, state, action, reward, terminated):
        if terminated:
            if state == self.finish_state:
                time.sleep(3)
                self.render_goal = False
                self.render_surface.blit(
                settings.TEXTURES['baterry-charge'],
                (settings.ROWS*30.5,
                    settings.VIRTUAL_HEIGHT - 33)
                )
                settings.SOUNDS['win'].play()
                
 
            else:
                time.sleep(3)
                self.tilemap.tiles[state].texture_name = "explosion"
                self.render_surface.blit(
                settings.TEXTURES['explosion'],
                (settings.ROWS*30.5,
                    settings.VIRTUAL_HEIGHT - 33)
                )
                self.render_surface.blit(
                settings.TEXTURES['explosion'],
                (self.tilemap.tiles[self.state].x,
                    self.tilemap.tiles[self.state].y)
                )
                self.render_character = False
                settings.SOUNDS['lost-game'].play()
                
        
        self.iteration += 1
        self.state = state
        self.action = action

    def render(self, current_battery):
        self.render_surface.fill((0, 0, 0))
        self.tilemap.render(self.render_surface)

        self.render_surface.blit(
            settings.TEXTURES['stool'],
            (self.tilemap.tiles[0].x, self.tilemap.tiles[0].y)
        )

        if self.render_goal:
            self.render_surface.blit(
                settings.TEXTURES['baterry-charge'],
                (self.tilemap.tiles[self.finish_state].x,
                 self.tilemap.tiles[self.finish_state].y)
            )

        if self.render_character:
            self.render_surface.blit(
                settings.TEXTURES['character'][self.action],
                (self.tilemap.tiles[self.state].x,
                 self.tilemap.tiles[self.state].y)
            )

        for _ in range(settings.ROWS + 1):
            self.render_surface.blit(
                settings.TEXTURES['background'],
                (_*31,
                    settings.VIRTUAL_HEIGHT - 30)
            )

        if (current_battery >= 92):
            self.render_surface.blit(
                settings.TEXTURES['battery5'],
                (settings.ROWS*30.5,
                    settings.VIRTUAL_HEIGHT - 33)
            )
        if (current_battery <= 91 and current_battery >= 80):
            self.render_surface.blit(
                settings.TEXTURES['battery4'],
                (settings.ROWS*30.5,
                 settings.VIRTUAL_HEIGHT - 33)
            )

        if (current_battery >= 50 and current_battery <= 79):
            self.render_surface.blit(
                settings.TEXTURES['battery3'],
                (settings.ROWS*30.5,
                 settings.VIRTUAL_HEIGHT - 33)
            )

        if (current_battery >= 30 and current_battery <= 49):
            self.render_surface.blit(
                settings.TEXTURES['battery0-3'],
                (settings.ROWS*30.5,
                 settings.VIRTUAL_HEIGHT - 33)
            )

        if (current_battery >= 20 and current_battery <= 29):
            self.render_surface.blit(
                settings.TEXTURES['battery0-2'],
                (settings.ROWS*30.5,
                 settings.VIRTUAL_HEIGHT - 33)
            )

        if (current_battery >= 10 and current_battery <= 29):
            self.render_surface.blit(
                settings.TEXTURES['battery0-1'],
                (settings.ROWS*30.5,
                 settings.VIRTUAL_HEIGHT - 33)
            )

        if (current_battery <= 9):
            self.render_surface.blit(
                settings.TEXTURES['baterry-lost-point'],
                (settings.ROWS*30.5,
                 settings.VIRTUAL_HEIGHT - 33)
            )

        self.screen.blit(
            pygame.transform.scale(
                self.render_surface,
                self.screen.get_size()),
            (0, 0)
        )

        # Texto del copy
        font = settings.FONTS['short-1']
        text_obj = font.render(f"{settings.COPY}", True, (0, 0, 0))
        text_rect = text_obj.get_rect()
        text_rect.center = (90, 513)
        self.screen.blit(text_obj, text_rect)
        # Texto del battery
        font = settings.FONTS['short']
        text_obj = font.render(f"{settings.BATTERY}", True, (0, 0, 0))
        text_rect = text_obj.get_rect()
        text_rect.center = (458, 513)
        self.screen.blit(text_obj, text_rect)
        # Texto STEPS
        font = settings.FONTS['short']
        text_obj = font.render(f"{settings.STEP}", True, (0, 0, 0))
        text_rect = text_obj.get_rect()
        text_rect.center = (270, 513)
        self.screen.blit(text_obj, text_rect)
        # Valor STEP
        font = settings.FONTS['short']
        text_obj = font.render(f"{self.iteration}", True, (69, 8, 153))
        text_rect = text_obj.get_rect()
        text_rect.center = (292, 513)
        self.screen.blit(text_obj, text_rect)

        pygame.event.pump()
        pygame.display.update()

    def close(self):
        pygame.font.quit()
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.display.quit()
        pygame.quit()
