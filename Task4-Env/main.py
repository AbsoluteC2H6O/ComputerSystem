#importar modulos
import time
import gym #standard API
from gym.envs.registration import register
from agent import ValueIteration
# registro Env
# register (
#     id="FrozenLake-v2",
#     entry_point="Env.frozen_lake:FrozenLakeEnv",
# )
register (
    id="Princess-v0",
    entry_point="Env.puzzles.v0.princess.princess:PrincessEnv",
)
    
# RobotBattery-v0, FrozenLake-v1, FrozenLake-v2
# env = gym.make('FrozenLake-v1', render_mode="human")
env = gym.make('Princess-v0', render_mode="human")
agent = ValueIteration(env.observation_space.n, env.action_space.n, env.P, 0.2)

# Elegir el modo Iteration o Policy
agent.solve(100, "Policy")
agent.render()

observation, info = env.reset()
terminated, truncated = False, False

env.render()
time.sleep(2)

while not (terminated or truncated):
    action = agent.get_action(observation)
    observation, current_reward, terminated, truncated, _, = env.step(action)
    if terminated and current_reward > 0:
        print("\n¡El agente completo con exito el juego!")
    elif terminated:
        print("\nEl agente NO completo el juego de manera exitosa, La estatua lo aplasto")

time.sleep(2)
env.close()