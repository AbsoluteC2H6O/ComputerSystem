import sys
import time

import gym
import matplotlib.pyplot as plt
import numpy as np
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


def run(env, agent, selection_method, episodes, total_rewards, total_average, position):
    i = 0
    valor = np.zeros(episodes)
    for episode in range(1, episodes + 1):
        # if episode % 10 == 0:
        #     print("Episode {} of {}".format(episode, episodes))
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
    total_average[position] = valor
    print('valor:', position, total_average[position])
    # total_alpha[position] = valor
    # print(total_rewards)
    # array_rewards[position] = total_rewards


def generateGraphics(env, episodes, alp):
    seedEps = [0.2]
    seedGmm = [0.95]

    s = (1, episodes)
    array_sarsa = np.zeros(s)
    array_expecteds = np.zeros(s)
    total_rewards_s = np.zeros(episodes)
    total_rewards_es = np.zeros(episodes)

    i = 0
    for eps in seedEps:
        for gam in seedGmm:
            print('Parametros: Epsilon = {}, Gamma = {}, Alpha = {}'.format(eps, gam, alp))
            # SARSA
            print("\nCalculo en modo SARSA")
            env.reset()
            agentSarsa = SARSA(
                calculate_states_size(env),
                env.action_space.n,
                alpha=alp,
                gamma=gam,
                epsilon=eps,
            )
            run(env, agentSarsa, "epsilon-greedy", episodes, total_rewards_s, array_sarsa, i)
            print("Completado el modo SARSA\n")
            env.reset()
            print("\nCalculo en modo EXPECTED SARSA\n")
            # EXPECTEDSARSA
            agentExpectedSarsa = EXPECTEDSARSA(
                calculate_states_size(env),
                env.action_space.n,
                alpha=alp,
                gamma=gam,
                epsilon=eps,
            )
            run(env, agentExpectedSarsa, "epsilon-greedy", episodes, total_rewards_es, array_expecteds, i)
            print("Completado el modo EXPECTED SARSA\n")
            print('Resultados de cada algoritmo:')
            print("\nSarsa:")
            agentSarsa.render()
            print("\nExpected Sarsa:")
            agentExpectedSarsa.render()
            # total_rewards_s, total_rewards_es = totalRewards(n_episodes=episodes)
            i += 1
    # printFigureIterable(array_sarsa, seedEps, seedGmm, alp, 0)
    # printFigureIterable(array_expecteds, seedEps, seedGmm, alp, 1)
    printPrueba(total_rewards_s, seedEps, seedGmm, alp, 0)
    printPrueba(total_rewards_es, seedEps, seedGmm, alp, 1)

def totalRewards(n_episodes):
    total_rewards_s = np.zeros(n_episodes)
    total_rewards_es = np.zeros(n_episodes)
    return total_rewards_s, total_rewards_es


def printFigureIterable(array_imp, seedEps, seedGmm, alp, cond):
    plt.figure(figsize=(12,8))
    iE = 0
    iA = 0
    for i in range(len(array_imp)):
        plt.plot(array_imp[i],
                label='E = {} G = {}'.format(seedEps[iE], seedGmm[iA]))
        iA += 1
        if iA == 4:
            iA = 0
            iE += 1

    plt.ylabel('Sum rewards')
    plt.xlabel('Episodes')
    plt.title('Parameters: Env = MountainCar, Alpha  = {}'.format(alp))
    plt.legend()
    if(cond == 0):
        plt.savefig("EnvMountainCarSarsa.jpg", dpi=600)
    else:
        plt.savefig("EnvMountainCarExpectedSarsa.jpg", dpi=600)
    #plt.show()


def printPrueba(array_imp, seedEps, seedGmm, alp, cond):
    plt.figure(figsize=(12,8))
    print('valor',array_imp)
    plt.plot(array_imp,
            label='E = {} G = {}'.format(seedEps, seedGmm))
    plt.ylabel('Sum rewards')
    plt.xlabel('Episodes')
    plt.title('Parameters: Env = MountainCar, Alpha  = {}'.format(alp))
    plt.legend()
    if(cond == 0):
        plt.savefig("PruebaSarsa.jpg", dpi=600)
    else:
        plt.savefig("PruebaExpectedSarsa.jpg", dpi=600)
    

def printFigure(total_alpha_s, total_alpha_es):
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
    episodes = 1000 if len(sys.argv) == 1 else int(sys.argv[1])

    env = gym.make("MountainCar-v0")
    total_rewards_s = np.zeros(episodes)
    total_alpha_s = np.zeros(10)
    total_rewards_es = np.zeros(episodes)
    total_alpha_es = np.zeros(10)
    seedAlp = 0.1
    eps = 0.2
    gam = 0.9
    # alp = 0.25

    # generateGraphics(env, episodes, alp)

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

        total_rewards_s, total_rewards_es = totalRewards(n_episodes=episodes)
        seedAlp += 0.1

    printFigure(total_alpha_s, total_alpha_es)
    env.close()
    # Play
    # env = gym.make("MountainCar-v0", render_mode="human")
    # run(env, agent, "greedy", 1)
    # agent.render()
    # env.close()