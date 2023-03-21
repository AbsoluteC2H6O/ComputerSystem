import gym
import time
import gym_environments
from gym.envs.registration import register
from agent import MonteCarlo
from agent_deterministic import MonteCarloDet
import numpy as np
import os
# registro Env
register (
    id="RobotMaze-v0",
    entry_point="Env.v0.robot_maze:RobotMazeEnv",
)
register (
    id="FrozenLake-v1",
    entry_point="Env.frozen_lake:FrozenLakeEnv",
)

# Allowing environment to have sounds
if "SDL_AUDIODRIVER" in os.environ:
    del os.environ["SDL_AUDIODRIVER"]


def train(env, agent, episodes):
    for _ in range(episodes):
        observation, _ = env.reset()
        # observation = np.random.randint(0, 4)
        terminated, truncated = False, False
        while not (terminated or truncated):
            action = agent.get_action(observation) # Accion aleatoria
            if action !=-1:
                new_observation, reward, terminated, truncated, _ = env.step(action)
                agent.update(observation, action, reward, terminated)
                observation = new_observation
            else:
                terminated = True
                
            

def play(env, agent):
    observation, _ = env.reset()
    terminated, truncated = False, False
    while not (terminated or truncated):
        action = agent.get_best_action(observation)
        if action !=-1:
            observation, _, terminated, truncated, _ = env.step(action)
            env.render()
        else:
            terminated = True
        time.sleep(1)


if __name__ == "__main__":
    env = gym.make("RobotMaze-v0", render_mode="human")
    # env = gym.make("FrozenLake-v1", render_mode="human")
    agent = MonteCarlo(
        env.observation_space.n, env.action_space.n, gamma=0.9, epsilon=0.9
    )

    agent_deterministic = MonteCarloDet(
        env.observation_space.n, env.action_space.n, gamma=0.9
    )

    mode = 'deterministic'
    if(mode == 'deterministic'):
        train(env, agent_deterministic, episodes=1000)
        agent_deterministic.render()
        play(env, agent_deterministic)

    else:
        train(env, agent, episodes=1000)
        agent.render()
        play(env, agent)
    env.render()
    env.close()