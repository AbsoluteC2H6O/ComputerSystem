import random
import time
import gym
from gym import spaces
import pygame

from . import settings

class Arm:
    def __init__(self, p=0, earn=0):
        self.probability = p
        self.earn = earn

    def execute(self):
        return self.earn if random.random() < self.probability else 0

class TwoArmedBanditEnv(gym.Env):
    def __init__(self):
        self.delay = 3
        self.arms = (Arm(0.5, 1), Arm(0.1, 100))
        self.observation_space = spaces.Discrete(1)
        self.action_space = spaces.Discrete(len(self.arms))
        pygame.init()
        pygame.display.init()
        self.window = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOWS_HEIGHT))
        pygame.display.set_caption("Two-Armed Bandit Environment")
        self.action = None
        self.reward = None
        self.rewards = 0

    def _get_obs(self):
        return 0

    def _get_info(self):
        return {'state': 0}

    def _get_rewards(self):
        if self.reward is None:
            return  self.rewards
        self.rewards += self.reward
        return self.rewards

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        if options is not None:
            if type(options) is not dict:
                raise RuntimeError("Variable options is not a dictionary")
            self.delay = options.get('delay', 0.5)

        observation = self._get_obs()
        info = self._get_info()
        return observation, info

    def step(self, action):
        self.action = action
        self.reward = self.arms[action].execute()
        observation = self._get_obs()
        info = self._get_info()
        rewards = self._get_rewards()
        self.render()   
        time.sleep(self.delay)

        return observation, self.reward, False, False, info

    def _render_props(self): #metodo privado
        if self.reward is None or self.action is None:
            return
        x = 50 + settings.MACHINE_WIDTH / 2

        if self.action == 1:
            x += 50 + settings.MACHINE_WIDTH

        # Render the first machine
        if(self.action == 0):
            self.window.blit(settings.TEXTURES['machine'], (50, 100)) 

        if(self.action == 1): 
        # Render the second machine
            self.window.blit(settings.TEXTURES['machine'], (100 + settings.MACHINE_WIDTH, 100))
        
        # Render the action
        arrow = settings.TEXTURES['arrow']
        w, h = arrow.get_size()
        self.window.blit(arrow, (x - w / 2 - 80, 150 +
                         settings.MACHINE_HEIGHT - h / 2))

        # Effect shade
        font = settings.FONTS['large']
        text_obj = font.render(f"{self.reward}", True, (0, 0, 0))
        text_rect = text_obj.get_rect()
        text_rect.center = (x+3, 83)
        self.window.blit(text_obj, text_rect)

        # Render the reward
        font = settings.FONTS['large']
        text_obj = font.render(f"{self.reward}", True, (234, 234, 77))
        text_rect = text_obj.get_rect()
        text_rect.center = (x, 80)
        self.window.blit(text_obj, text_rect)

        # Render the rewards
        font = settings.FONTS['large']
        text_obj = font.render(f"{self.rewards}", True, (0, 0, 0))
        text_rect = text_obj.get_rect()
        text_rect.center = (300, 80)
        self.window.blit(text_obj, text_rect)

        # Copy
        font = settings.FONTS['short']
        text_obj = font.render(settings.TEXT, True, (0, 0, 0))
        text_rect = text_obj.get_rect()
        text_rect.center = (200, 30)
        self.window.blit(text_obj, text_rect)

    def render(self):
        self.window.fill((144, 48, 188))
        self._render_props()

        pygame.event.pump()
        pygame.display.update()

    def close(self):
        pygame.display.quit()
        pygame.font.quit()
        pygame.quit()
