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
        # Generate P matrix
        MatrixP = {state: {action: [] for action in range(
            self.action_space.n)} for state in range(self.observation_space.n)}
        ifEndsGame = False
        for princessPos in range(self.n):
            for st1Position in range(self.n):
                for st2Position in range(self.n):
                    stateByPosInit = princessPos * self.n**2 + st1Position*self.n + st2Position*1

                    # Logica de las acciones
                    # 0: left, 1: down, 2: right, 3: up
                    for action in range(4):
                        stateByPosEnd = stateByPosInit
                        princessPosInitCoordinate = self.calculateCoordinate(
                            princessPos)
                        st1posInitCoordinate = self.calculateCoordinate(
                            st1Position)
                        st2posInitCoordinate = self.calculateCoordinate(
                            st2Position)
                        princessPosEndCoordinate = princessPosInitCoordinate
                        st1posEndCoordinate = st1posInitCoordinate
                        st2posEndCoordinate = st2posInitCoordinate
                        if (action == 0):
                            if (self.princessCanMove(princessPos, st1posInitCoordinate, st2posInitCoordinate, action)):
                                princessPosEndCoordinate = self.coordinateLeft(
                                    princessPos)
                            if (self.Status1CanMove(st1posInitCoordinate, st2posInitCoordinate, action)):
                                st1posEndCoordinate = self.coordinateRight(
                                    st1Position)
                            if (self.Status2CanMove(st1posInitCoordinate, st2posInitCoordinate, action)):
                                st2posEndCoordinate = self.coordinateLeft(
                                    st2Position)
                            if (st2posEndCoordinate == st1posEndCoordinate):
                                st1posEndCoordinate = st1posInitCoordinate
                                st2posEndCoordinate = st2posInitCoordinate
                        if (action == 1):
                            if (self.princessCanMove(princessPos, st1posInitCoordinate, st2posInitCoordinate, action)):
                                princessPosEndCoordinate = self.coordinateDown(
                                    princessPos)
                            if (self.Status1CanMove(st1posInitCoordinate, st2posInitCoordinate, action)):
                                st1posEndCoordinate = self.coordinateUp(
                                    st1Position)
                            if (self.Status2CanMove(st1posInitCoordinate, st2posInitCoordinate, action)):
                                st2posEndCoordinate = self.coordinateDown(
                                    st2Position)
                            if (st2posEndCoordinate == st1posEndCoordinate):
                                st1posEndCoordinate = st1posInitCoordinate
                                st2posEndCoordinate = st2posInitCoordinate
                        if (action == 2):
                            if (self.princessCanMove(princessPos, st1posInitCoordinate, st2posInitCoordinate, action)):
                                princessPosEndCoordinate = self.coordinateRight(
                                    princessPos)
                            if (self.Status1CanMove(st1posInitCoordinate, st2posInitCoordinate, action)):
                                st1posEndCoordinate = self.coordinateLeft(
                                    st1Position)
                            if (self.Status2CanMove(st1posInitCoordinate, st2posInitCoordinate, action)):
                                st2posEndCoordinate = self.coordinateRight(
                                    st2Position)
                            if (st2posEndCoordinate == st1posEndCoordinate):
                                st1posEndCoordinate = st1posInitCoordinate
                                st2posEndCoordinate = st2posInitCoordinate
                        if (action == 3):
                            if (self.princessCanMove(princessPos, st1posInitCoordinate, st2posInitCoordinate, action)):
                                princessPosEndCoordinate = self.coordinateUp(
                                    princessPos)
                            if (self.Status1CanMove(st1posInitCoordinate, st2posInitCoordinate, action)):
                                st1posEndCoordinate = self.coordinateDown(
                                    st1Position)
                            if (self.Status2CanMove(st1posInitCoordinate, st2posInitCoordinate, action)):
                                st2posEndCoordinate = self.coordinateUp(
                                    st2Position)
                            if (st2posEndCoordinate == st1posEndCoordinate):
                                st1posEndCoordinate = st1posInitCoordinate
                                st2posEndCoordinate = st2posInitCoordinate

                        princessPosEndState = self.calculateStateByCoordinate(
                            princessPosEndCoordinate)
                        st1posEndState = self.calculateStateByCoordinate(
                            st1posEndCoordinate)
                        st2posEndState = self.calculateStateByCoordinate(
                            st2posEndCoordinate)

                        stateByPosEnd = self.__compute_state_result(
                            princessPosEndState, st1posEndState, st2posEndState)

                        reward = 0
                        # Logica de las reglas
                        rule1 = False
                        rule2 = False
                        rule3 = False
                        rule4 = False
                        rule5 = False
                        # 1- Una transición que me lleve de s a s' con s != s'  tiene recompensa de -1.
                        if (stateByPosEnd != stateByPosInit):
                            rule1 = True
                        # 2- Una transición que me lleve de s a s' con s == s'  tiene recompensa de -10.
                        else:
                            rule2 = True

                        # 3- Una transición que me lleve de a un estado tal en el que la posición del
                        # personaje sea igual a la de una de las estatuas, tiene recompensa -100 y debe
                        # ser marcado en True el cuarto componente de la tupla.
                        if (princessPosEndCoordinate == st1posEndCoordinate or princessPosEndCoordinate == st2posEndCoordinate):
                            rule3 = True

                        # 4- Una transición que me lleve a un estado tal en el que las estatuas estén ubicadas
                        # sobre ambos targets al mismo tiempo, tiene recompensa 1000 y debe ser marcado en True
                        # el cuarto componente de la tupla.
                        if (self.check_win(st1posEndCoordinate, st2posEndCoordinate)):
                            rule4 = True

                        if (self.check_win(st1posInitCoordinate, st2posInitCoordinate)):
                            rule5 = True

                        if (rule3):
                            reward = -100
                        elif (rule4):
                            reward = 1000
                            ifEndsGame = stateByPosEnd
                        elif (rule2):
                            reward = -10
                        else:
                            reward = -1

                        status = False

                        if (rule3 == True):
                            status = True
                        elif (rule4 == True):
                            status = True
                        # 5. Cualquier acción de ejecutada desde un estado terminal me deja en el mismo estado
                        # con recompensa 0.
                        if (stateByPosInit == ifEndsGame and ifEndsGame!=False):
                            MatrixP[stateByPosInit][action].append(
                                (1.0, stateByPosInit, 0.0, True))
                        else:
                            MatrixP[stateByPosInit][action].append(
                                (1.0, stateByPosEnd, reward, status))

        f = open("matrixP.py", "a")
        f.write(str(MatrixP))
        f.close()
        return MatrixP

    def calculateCoordinate(self, stOrChState):
        row = stOrChState // self.game.world.tile_map.cols
        column = (stOrChState-self.game.world.tile_map.cols*row)
        position = [row, column]
        return position

    def coordinateUp(self, stOrChState):
        row = (stOrChState // self.game.world.tile_map.cols)
        column = (stOrChState-self.game.world.tile_map.cols*row)
        if ((row - 1) >= 0 and row < self.game.world.tile_map.rows and column >= 0 and column < self.game.world.tile_map.cols):
            if (self.game.world.tile_map.map[row-1][column] != 0):
                row = row - 1
        position = [row, column]
        return position

    def coordinateDown(self, stOrChState):
        row = (stOrChState // self.game.world.tile_map.cols)
        column = (stOrChState-self.game.world.tile_map.cols*row)
        if ((row + 1) < self.game.world.tile_map.rows and row >= 0 and column >= 0 and column < self.game.world.tile_map.cols):
            if (self.game.world.tile_map.map[row+1][column] != 0):
                row = row + 1
        position = [row, column]
        return position

    def coordinateRight(self, stOrChState):
        row = (stOrChState // self.game.world.tile_map.cols)
        column = (stOrChState-self.game.world.tile_map.cols*row)
        if ((column + 1) < self.game.world.tile_map.cols and (column + 1) >= 0 and row >= 0 and row < self.game.world.tile_map.rows):
            if (self.game.world.tile_map.map[row][column+1] != 0):
                column = column + 1
        position = [row, column]
        return position

    def coordinateLeft(self, stOrChState):
        row = (stOrChState // self.game.world.tile_map.cols)
        column = (stOrChState-self.game.world.tile_map.cols*row)
        if ((column - 1) >= 0 and (column - 1) < self.game.world.tile_map.cols and row >= 0 and row < self.game.world.tile_map.rows):
            if (self.game.world.tile_map.map[row][column-1] != 0):
                column = column - 1
        position = [row, column]
        return position

    def princessCanMove(self, prPos, st1Pos, st2Pos, action):
        row = (prPos // self.game.world.tile_map.cols)
        column = (prPos-self.game.world.tile_map.cols*row)
        if (action == 3):
            row = row-1
        if (action == 2):
            column = column+1
        if (action == 1):
            row = row+1
        if (action == 0):
            column = column-1

        if (row != st1Pos[0] and row != st2Pos[0] and column != st1Pos[1] and column != st2Pos[1]):
            return True
        else:
            return False

    def Status1CanMove(self, st1Pos, st2Pos, action):
        r1 = st1Pos[0]
        c1 = st1Pos[1]
        r2 = st2Pos[0]
        c2 = st2Pos[1]

        if (action == 3):
            r1 = r1-1
        if (action == 2):
            c1 = c1+1
        if (action == 1):
            r1 = r1+1
        if (action == 0):
            c1 = c1-1

        if (c1 != c2 and r1 != r2):
            return True
        else:
            return False

    def Status2CanMove(self, st1Pos, st2Pos, action):
        r1 = st1Pos[0]
        c1 = st1Pos[1]
        r2 = st2Pos[0]
        c2 = st2Pos[1]

        if (action == 3):
            r1 = r1-1
            r2 = r2+1
        if (action == 2):
            c1 = c1+1
            c2 = c2-1
        if (action == 1):
            r1 = r1+1
            r2 = r2-1
        if (action == 0):
            c1 = c1-1
            c2 = c2+1

        if (c1 != c2 and r1 != r2):
            return True
        else:
            return False

    def calculateStateByCoordinate(self, coordinate):
        state = int(coordinate[1] +
                    self.game.world.tile_map.cols*coordinate[0])
        return state

    def check_win(self, statue_1, statue_2):
        s1 = statue_1[0], statue_1[1]
        s2 = statue_2[0], statue_2[1]
        t1 = self.game.world.target_1
        t2 = self.game.world.target_2
        return (s1 == t1 and s2 == t2) or (s1 == t2 and s2 == t1)

    def render(self):
        self.game.render()

    def close(self):
        self.game.close()
