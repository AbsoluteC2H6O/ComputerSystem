#importar modulos
import os
import time
import gym #standard API
from gym.envs.registration import register
from agent import ValueIteration
# registro Env: "Env.v0.robot_maze:RobotMazeEnv"," / ""
register (
    id="RobotBattery-v0",
    entry_point="Env.v0.robot_battery:RobotBatteryEnv",
)

# Allowing environment to have sounds
if "SDL_AUDIODRIVER" in os.environ:
    del os.environ["SDL_AUDIODRIVER"]

# RobotBattery-v0, FrozenLake-v1, FrozenLake-v2, RobotMaze-V0
env = gym.make('RobotBattery-v0', render_mode="human")
agent = ValueIteration(env.observation_space.n, env.action_space.n, env.P, 0.9)

agent.solve(1000)
agent.render()

observation, info = env.reset()
terminated, truncated = False, False

env.render()
time.sleep(1)

while not (terminated or truncated):
    action = agent.get_action(observation)
    observation, _, terminated, truncated, _ = env.step(action)

time.sleep(1)
env.close()