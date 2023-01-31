import time
import numpy as np
import gym
from gym import spaces
import pygame
from . import settings
from .world import World


class RobotBatteryEnv(gym.Env):
    # metadata = {"render_modes": ["human"], "render_fps": 4}
    def __init__(self, render_mode=None):
        self.observation_space = spaces.Discrete(settings.NUM_TILES)
        self.action_space = spaces.Discrete(settings.NUM_ACTIONS)
        self.current_action = 1
        self.current_state = 0
        self.current_reward = 0.0
        self.delay = settings.DEFAULT_DELAY
        self.P = settings.P
        self.world = World(
            "Robot  Battery Environment",
            self.current_state,
            self.current_action
        )
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        if options is not None:
            if not isinstance(options, dict):
                raise RuntimeError("Variable options is not a dictionary")
            self.delay = options.get('delay', 0.5)
        np.random.seed(seed)
        self.current_state = 0
        self.current_action = 1
        self.world.reset(self.current_state, self.current_action)
        # Agent robot
        self.action = 0
        self.reward = 0.0
        self.state = 0
        return self.state, {}

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

        self.world.update(
            self.current_state,
            self.current_action,
            self.current_reward,
            terminated
        )
        
        self.action = action
        self.reward = self.P[self.state][action][0][2]
        terminated = self.P[self.state][action][0][3]
        self.state = self.P[self.state][action][0][1]
        
        self.render()
        time.sleep(self.delay)

        return self.current_state, self.current_reward, terminated, False, {}
        #
   

    def render(self):
        self.world.render()
        # print(
        #     "Action {}, reward {}, state {}".format(
        #         self.action,
        #         self.reward,
        #         self.state))
    def close(self):
        self.world.close()