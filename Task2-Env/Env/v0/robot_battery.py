import time
import numpy as np
import gym
from gym import spaces
import pygame
from . import settings
from .world import World


class RobotBatteryEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, **kwargs):
        self.observation_space = spaces.Discrete(settings.NUM_TILES)
        self.action_space = spaces.Discrete(settings.NUM_ACTIONS)
        self.current_action = 1
        self.current_state = 0
        self.current_reward = 0.0
        self.decrement_battery = 5
        self.current_battery = 100
        self.initial_battery = 100
        self.delay = settings.DEFAULT_DELAY
        self.P = settings.P
        self.world = World(
            "Robot Battery Environment",
            self.current_state,
            self.current_action
        )

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        if options is not None:
            if not isinstance(options, dict):
                raise RuntimeError("Variable options is not a dictionary")
            self.delay = options.get('delay', 0.2)

        np.random.seed(seed)

        self.current_state = 0
        self.current_action = 1
        self.world.reset(self.current_state, self.current_action)

        return 0, {}

    def step(self, action):
        self.current_action = action

        possibilities = self.P[self.current_state][self.current_action]

        p = 0
        i = 0

        r = np.random.random()

        while r > p:
            r -= p
            p, self.current_state, self.current_reward, terminated = possibilities[i]
            i += 1
        print("Valor de i: ", i)
        if r < 1 - (self.current_battery / self.initial_battery):
            print("Valor de current_battery:", self.current_battery)
            if(i >= 2):
                if(self.current_action == 1):
                    self.current_action = 2
                    p, self.current_state, self.current_reward, terminated = possibilities[0]
            else:
                p, self.current_state, self.current_reward, terminated = possibilities[i]

        self.world.update(
            self.current_state,
            self.current_action,
            self.current_reward,
            terminated
        )

        if(self.current_battery <= self.decrement_battery):
            settings.SOUNDS['lost-game'].play()
            time.sleep(self.delay+1)
            return self.current_state, self.current_reward, True, True, {}
        else:
            self.current_battery -= self.decrement_battery

        self.render()
        time.sleep(self.delay)

        return self.current_state, self.current_reward, terminated, False, {}

    def render(self):
        self.world.render()

    def close(self):
        self.world.close()
