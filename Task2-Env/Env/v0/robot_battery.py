import time
import numpy as np
import gym
from gym import spaces
import pygame
from . import settings
from .world import World


class RobotBatteryEnv(gym.Env):

    def __init__(self, render_mode=None):
        super().__init__()
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Discrete(6)
        self.P =settings.P
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.action = 0
        self.reward = 0.0
        self.state = 0
        return self.state, {}

    def step(self, action):
        self.action = action
        self.reward = self.P[self.state][action][0][2]
        terminated = self.P[self.state][action][0][3]
        self.state = self.P[self.state][action][0][1]
        self.render()
        time.sleep(1)
        return self.state, self.reward, terminated, False, {}

    def render(self):
        print(
            "Action {}, reward {}, state {}".format(
                self.action,
                self.reward,
                self.state))