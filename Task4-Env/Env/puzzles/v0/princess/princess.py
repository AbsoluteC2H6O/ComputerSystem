import time
import numpy as np
import pygame
import gym
from gym import spaces
from .game.Game import Game

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
        MatrixP = {state: {action: [] for action in range(self.action_space.n)} for state in range(self.observation_space.n)}
        # 0: left, 1: down, 2: right, 3: up
        for ch in range(self.n ):
            for st1 in range(self.n):
                for st2 in range(self.n):
                    statePos = ch * self.n**2+st1*self.n+st2
                    # print("state",statePos )
                    for action in range(4):
                        # emular juego con MOVE CHECK_WIN CHECK_LOSS
                        # decidir valores para la tupla
                        # Como ponerlos en una posicion inicial: main character y estatuas.
                        
                        # if(action ==0):
                        # if(action ==1):
                        # if(action ==2):
                        # if(action ==3):
                        # Como modelar movimiento de las estatuas
                        self.sumlateGame()
                        loss = self.game.world.check_lost()
                        win = self.game.world.check_win()

                        reward = 0
                        # Generar la logica de las reglas
                        rule1 = False
                        rule2 = False
                        rule3 = False
                        rule4 = False
                        rule5 = False

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

                        if (loss == True):
                            status = True
                        elif (win == True):
                            status = True
                        if (rule3 == True):
                            status = True
                        # Generar una logica para los estados
                        # newState = statePos
                        # if (rule1):
                        #     newState += 1
                        MatrixP[statePos][action].append((1.0, statePos, reward, status))
                        # print('loss', loss)
                        # print('win', win)
        print("ma", MatrixP)
        return MatrixP

    def calculateCoordinate(self, stOrChState):
        row = stOrChState // self.game.world.tile_map.cols
        column = (stOrChState-self.game.world.tile_map.cols*row)
        position = [row, column]
        return position
    
    def sumlateGame(self):
        print("Start simulating")
        
    def render(self):
        self.game.render()

    def close(self):
        self.game.close()
