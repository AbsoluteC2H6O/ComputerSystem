import sys
import time
import gym
import gym_environments
import numpy as np
import matplotlib.pyplot as plt
from agentSarsa import SARSA
from agentSarsaE import EXPECTEDSARSA

def calculate_states_size(env):
    max = env.observation_space.high
    min = env.observation_space.low
    sizes = (max - min) * np.array([10, 100]) + 1
    return int(sizes[0]) * int(sizes[1])


def calculate_state(env, value):
    min = env.observation_space.low
    values = (value - min) * np.array([10, 100])
    return int(values[1]) * 19 + int(values[0])


def run(env, agent, selection_method, episodes, total_rewards, total_alpha, position):
    i = 0
    for episode in range(1, episodes + 1):
        if episode % 10 == 0:
            print("Episode {} of {}".format(episode, episodes))
        observation, _ = env.reset()
        action = agent.get_action(calculate_state(env, observation), selection_method)
        terminated, truncated = False, False
        while not (terminated or truncated):
            new_observation, reward, terminated, truncated, _ = env.step(action)
            next_action = agent.get_action(
                calculate_state(env, new_observation), selection_method
            )
            agent.update(
                calculate_state(env, observation),
                action,
                calculate_state(env, new_observation),
                next_action,
                reward,
                terminated,
                truncated,
            )
            observation = new_observation
            action = next_action
            total_rewards[i] += reward
        i += 1
    valor = np.average(total_rewards)
    print('valor', valor)
    total_alpha[position] = valor


def totalRewards(n_episodes):
    total_rewards_s = np.zeros(n_episodes)
    total_rewards_es = np.zeros(n_episodes)
    return total_rewards_s, total_rewards_es


def printFigure(total_alpha_s, total_alpha_es):
    # window = 5
    # q_avg_rewards = np.array([np.mean(total_rewards_s[i-window:i])  
    #                         if i >= window
    #                         else np.mean(total_rewards_s[:i])
    #                         for i in range(1, len(total_rewards_s))
    #                         ])
    # dq_avg_rewards = np.array([np.mean(total_rewards_es[i-window:i])  
    #                         if i >= window
    #                         else np.mean(total_rewards_es[:i])
    #                         for i in range(1, len(total_rewards_es))
    #                         ])
    plt.figure(figsize=(10,6))
    plt.plot(total_alpha_s,
            label='Sarsa')
    plt.plot(total_alpha_es,
            label='ExpectedSarsa')
    plt.ylabel('Average return')
    plt.xlabel('Alpha')
    plt.title('Parameters: Env = MountainCar, Epsilon = 0.1, Gamma = 0.9')
    plt.legend(loc='lower center', ncol=3, frameon=False)
    plt.savefig("EnvMountainCarAlpha.jpg", dpi=600)
    #plt.show()

if __name__ == "__main__":
    episodes = 50 if len(sys.argv) == 1 else int(sys.argv[1])

    env = gym.make("MountainCar-v0")

    total_rewards_s = np.zeros(episodes)
    total_alpha_s = np.zeros(10)
    total_rewards_es = np.zeros(episodes)
    total_alpha_es = np.zeros(10)
    episodeReward = 0
    seedAlp = 0.1
    eps = 0.1
    gam = 0.9

    for i in range(10):
        print('Parametros: Epsilon = {}, Gamma = {}, Alpha = {}'.format(eps, gam, seedAlp))
        # SARSA
        print("\nCalculo en modo SARSA")
        env.reset()
        agentSarsa = SARSA(
            calculate_states_size(env),
            env.action_space.n,
            alpha=seedAlp,
            gamma=gam,
            epsilon=eps,
        )
        run(env, agentSarsa, "epsilon-greedy", episodes, total_rewards_s, total_alpha_s, i)
        print("Completado el modo SARSA\n")
        env.reset()
        print("\nCalculo en modo EXPECTED SARSA\n")
        # EXPECTEDSARSA
        agentExpectedSarsa = EXPECTEDSARSA(
            calculate_states_size(env),
            env.action_space.n,
            alpha=seedAlp,
            gamma=gam,
            epsilon=eps,
        )
        run(env, agentExpectedSarsa, "epsilon-greedy", episodes, total_rewards_es, total_alpha_es, i)
        print("Completado el modo EXPECTED SARSA\n")
        print('Resultados de cada algoritmo:')
        print("\nSarsa:")
        agentSarsa.render()
        print("\nExpected Sarsa:")
        agentExpectedSarsa.render()
        total_rewards_s, total_rewards_es = totalRewards(n_episodes=episodes)
        seedAlp += 0.1

    printFigure(total_alpha_s, total_alpha_es)
    env.close()
        # Play
        # env = gym.make("MountainCar-v0", render_mode="human")
        # run(env, agent, "greedy", 1)
        # agent.render()
        # env.close()