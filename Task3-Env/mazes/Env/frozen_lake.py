import time
import numpy as np
import gym
from gym import spaces
import pygame
from . import settings
from .world import World
import maze_generators
class FrozenLakeEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, **kwargs):
        super().__init__()
        self.observation_space = spaces.Discrete(settings.NUM_TILES)
        self.action_space = spaces.Discrete(settings.NUM_ACTIONS)
        self.current_action = 0
        self.current_state = 0
        self.current_reward = 0.0
        self.delay = settings.DEFAULT_DELAY
        # Maze
        self._rows = kwargs.get("rows", 5)
        self._cols = kwargs.get("cols", 5)
        maze_generator = kwargs.get(
            "maze_generator_class", maze_generators.KruskalMazeGenerator
        )(self._rows, self._cols)
        self.walls = maze_generator.generate()
        self.P = maze_generator.generatePMatrix()
        self.world = World(
            "Frozen Lake Environment",
            self.current_state,
            self.current_action,
            self.P,
        )
        # self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        # self.action = 0
        # self.reward = 0.0
        # self.state = 0
        if options is not None:
            if not isinstance(options, dict):
                raise RuntimeError("Variable options is not a dictionary")
            self.delay = options.get('delay', 0.5)

        np.random.seed(seed)
        self.current_state = 0
        self.current_action = 0
        self.world.reset(self.current_state, self.current_action)
        return 0, {}

    def step(self, action):
        self.current_action = action
        # self.action = action
        # self.reward = self.P[self.state][action][0][2]
        _, self.current_state, self.current_reward, terminated = self.P[self.current_state][self.current_action][0]
        # self.state = self.P[self.state][action][0][1]
        
        self.world.update(
            self.current_state,
            self.current_action,
            self.current_reward,
            terminated
        )

        self.render()
        time.sleep(self.delay)

        return self.current_state, self.current_reward, terminated, False, {}

    def render(self):
        print(
            "Action {}, reward {}, state {}".format(
                self.current_action, self.current_reward, self.current_state
            )
        )
        print("-" * int(self._cols * 2 + 1))
        for i in range(self._rows):
            for j in range(self._cols):
                # evaluate if there is a left wall
                current_index = i * self._cols + j
                left_index = i * self._cols + j - 1
                has_left_wall = (
                    j == 0
                    or (current_index, left_index) in self.walls
                    or (left_index, current_index) in self.walls
                )

                # render the left wall if exists
                if has_left_wall:
                    print("|", end="")
                else:
                    # space if there is no a left wall
                    print(" ", end="")

                # render the cell
                print(' ', end="")

            # render the right wall for the current row
            print("|")

            # render the first bottom wall
            print("-", end="")

            # render the bottom wall when if exists
            for j in range(self._cols):
                current_index = i * self._cols + j
                bottom_index = (i + 1) * self._cols + j
                has_bottom_wall = (
                    i == self._rows - 1
                    or (current_index, bottom_index) in self.walls
                    or (bottom_index, current_index) in self.walls
                )
                if has_bottom_wall:
                   print("-", end="")
                else:
                    # space if there is not a bottom wall
                    print(" ", end="")
                
                # render the next bottom wall
                print("-", end="")

            # finally, end of line
            print("")
        self.world.render()

    def close(self):
        self.world.close()
