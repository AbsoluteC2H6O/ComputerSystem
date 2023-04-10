import time
import numpy as np
import pygame
import gym
from gym import spaces
from .game.Game import Game
from Env.puzzles.v0.princess.game import settings


class PrincessEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, **kwargs):
        super().__init__()
        self.render_mode = kwargs.get("render_mode")
        self.game = Game("Princess Puzzle Env", self.render_mode)
        self.n = self.game.world.tile_map.rows * self.game.world.tile_map.cols
        self.observation_space = spaces.Discrete(self.n * self.n * self.n)
        self.action_space = spaces.Discrete(4)
        self.current_state = self.game.get_state()
        self.current_action = 0
        self.current_reward = 0.0
        self.delay = 1
        self.rows = 0
        self.cols = 0
        with open(settings.ENVIRONMENT, "r") as f:
            self.rows, self.cols = f.readline().split(" ")
        self.rows = int(self.rows)
        self.cols = int(self.cols)
        self.P = self.generateP()

    def __compute_state_result(self, mc, s1, s2):
        return mc * self.n**2 + s1 * self.n + s2

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        if options is not None:
            if not isinstance(options, dict):
                raise RuntimeError("Variable options is not a dictionary")
            self.delay = options.get("delay", 0.5)

        np.random.seed(seed)

        self.current_state = self.game.reset()
        self.current_action = 0
        self.current_reward = 0

        return self.__compute_state_result(*self.current_state), {}

    def step(self, action):
        # Modifiquen el método step para que use la tabla P en lugar de poner las estructuras condicionales.
        # Luego modifiquen el método step para que use la tabla P en lugar de poner las estructuras condicionales.
        self.current_action = action

        old_state = self.current_state
        self.current_state = self.game.update(self.current_action)

        terminated = False
        self.current_reward = -1.0

        if old_state == self.current_state:
            self.current_reward = -10.0
        elif self.game.world.check_lost():
            terminated = True
            self.current_reward = -100.0
        elif self.game.world.check_win():
            terminated = True
            self.current_reward = 1000.0

        if self.render_mode is not None:
            self.render()
            time.sleep(self.delay)

        return (
            self.__compute_state_result(*self.current_state),
            self.current_reward,
            terminated,
            False,
            {},
        )

    def generateP(self):
        print("Generating P matrix")
        # Reglas:
        # 1- Una transición que me lleve de s a s' con s != s'  tiene recompensa de -1.
        # 2- Una transición que me lleve de s a s' con s == s'  tiene recompensa de -10.
        # 3- Una transición que me lleve de a un estado tal en el que la posición del
        # personaje sea igual a la de una de las estatuas, tiene recompensa -100 y debe
        # ser marcado en True el cuarto componente de la tupla.
        # 4- Una transición que me lleve a un estado tal en el que las estatuas estén ubicadas
        # sobre ambos targets al mismo tiempo, tiene recompensa 1000 y debe ser marcado en True
        # el cuarto componente de la tupla.
        # 5. Cualquier acción de ejecutada desde un estado terminal me deja en el mismo estado
        # con recompensa 0.

        # Generate P matrix
        MatrixP = {state: {action: [] for action in range(
            self.action_space.n)} for state in range(self.observation_space.n)}

        for princessPos in range(self.n):
            for st1Position in range(self.n):
                for st2Position in range(self.n):
                    stateByPosInit = princessPos * self.n**2+st1Position*self.n+st2Position
                    princessPosInitCoordinate = self.calculateCoordinate(
                        princessPos)
                    st1posInitCoordinate = self.calculateCoordinate(
                        st1Position)
                    st2posInitCoordinate = self.calculateCoordinate(
                        st2Position)
                    # Logica de las acciones
                    # 0: left, 1: down, 2: right, 3: up
                    for action in range(4):
                        princessPosEndCoordinate = princessPosInitCoordinate
                        st1posEndCoordinate = st1posInitCoordinate
                        st2posEndCoordinate = st2posInitCoordinate

                        if (action == 0):
                            princessPosEndCoordinate = self.coordinateLeft(
                                princessPos)
                            st1posEndCoordinate = self.coordinateLeft(
                                st1Position)
                            st2posEndCoordinate = self.coordinateRight(
                                st2Position)
                        if (action == 1):
                            princessPosEndCoordinate = self.coordinateDown(
                                princessPos)
                            st1posEndCoordinate = self.coordinateDown(
                                st1Position)
                            st2posEndCoordinate = self.coordinateUp(
                                st2Position)
                        if (action == 2):
                            princessPosEndCoordinate = self.coordinateRight(
                                princessPos)
                            st1posEndCoordinate = self.coordinateRight(
                                st1Position)
                            st2posEndCoordinate = self.coordinateLeft(
                                st2Position)
                        if (action == 3):
                            princessPosEndCoordinate = self.coordinateUp(
                                princessPos)
                            st1posEndCoordinate = self.coordinateUp(
                                st1Position)
                            st2posEndCoordinate = self.coordinateDown(
                                st2Position)

                        princessPosEndState = self.calculateStateByCoordinate(
                            princessPosEndCoordinate)
                        st1posEndState = self.calculateStateByCoordinate(
                            st1posEndCoordinate)
                        st2posEndState = self.calculateStateByCoordinate(
                            st2posEndCoordinate)

                        stateByPosEnd = princessPosEndState * self.n**2 + st1posEndState*self.n+st2posEndState

                        reward = 0
                        # Logica de las reglas
                        rule1 = False
                        rule2 = False
                        rule3 = False
                        rule4 = False
                        rule5 = False
                        if(stateByPosEnd != stateByPosInit):
                            rule1 = True
                        else:
                            rule2 = True
                            
                        if(princessPosEndCoordinate == st1posEndCoordinate or princessPosEndCoordinate == st2posEndCoordinate):
                            rule3 =True

                        if(self.check_win(st1posEndCoordinate,st2posEndCoordinate)):
                            rule4 =True
                            
                        if(self.check_win(st1posInitCoordinate,st2posInitCoordinate)):
                            rule5 =True
                            
                        if (rule1):
                            reward = -1
                        elif (rule2):
                            reward = -10
                        elif (rule3):
                            reward = -100
                        elif (rule4):
                            reward = 1000
                        elif (rule5):
                            reward = 0

                        status = False

                        if (rule3 == True):
                            status = True
                        elif (rule4 == True):
                            status = True
                        MatrixP[stateByPosInit][action].append(
                            (1.0, stateByPosEnd, reward, status))
                     
        print("ma", MatrixP)
        return MatrixP

    def calculateCoordinate(self, stOrChState):
        row = stOrChState // self.game.world.tile_map.cols
        column = (stOrChState-self.game.world.tile_map.cols*row)
        position = [row, column]
        return position

    def coordinateLeft(self, stOrChState):
        row = (stOrChState // self.game.world.tile_map.cols)
        column = (stOrChState-self.game.world.tile_map.cols*row)
        if (row - 1 > 0):
            if (self.game.world.tile_map.map[row-1][column] != 0):
                row = row - 1
        position = [row, column]
        return position

    def coordinateRight(self, stOrChState):
        row = (stOrChState // self.game.world.tile_map.cols)
        column = (stOrChState-self.game.world.tile_map.cols*row)
        if (row + 1 < self.rows):
            if (self.game.world.tile_map.map[row+1][column] != 0):
                row = row + 1
        position = [row, column]
        return position

    def coordinateDown(self, stOrChState):
        row = (stOrChState // self.game.world.tile_map.cols)
        column = (stOrChState-self.game.world.tile_map.cols*row)
        if (column + 1 < self.cols):
            if (self.game.world.tile_map.map[row][column+1] != 0):
                column + 1
        position = [row, column]
        return position

    def coordinateUp(self, stOrChState):
        row = (stOrChState // self.game.world.tile_map.cols)
        column = (stOrChState-self.game.world.tile_map.cols*row)
        if (column - 1 > 0):
            if (self.game.world.tile_map.map[row][column-1] != 0):
                column - 1
        position = [row, column]
        return position

    def calculateStateByCoordinate(self, coordinate):
        state = coordinate[1] + self.game.world.tile_map.cols*coordinate[0]
        return state

    def check_win(self, statue_1, statue_2):
        s1 = statue_1[0], statue_1[1]
        s2 = statue_2[0], statue_2[1]
        t1 = self.game.world.target_1
        t2 = self.game.world.target_2
        return s1 == t1 and s2 == t2
    
    def render(self):
        self.game.render()

    def close(self):
        self.game.close()
