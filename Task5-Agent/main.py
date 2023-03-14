import sys
import time
import gym
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


def run(env, agent, selection_method, episodes, total_rewards, total_average, position):
    i = 0
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
    # print('valor total', total_average[position], position)
    # total_alpha[position] = valor
    # print(total_rewards)
    # total_average[position] = total_rewards
    print('valor total', total_average[position], position)

def generateGraphics(env, episodes, alp):
    seedEps = [0.05, 0.3, 0.6]
    seedGmm = [0.2, 0.5, 0.8]

    s = (len(seedEps)*len(seedGmm), episodes)
    array_sarsa = np.zeros(s)
    array_expecteds = np.zeros(s)
    total_rewards_s = np.zeros(episodes)
    total_rewards_es = np.zeros(episodes)

    i = 0
    for eps in seedEps:
        for gam in seedGmm:
            print('\nParametros: Epsilon = {}, Gamma = {}, Alpha = {}'.format(eps, gam, alp))
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
            print("Completado el modo SARSA")
            env.reset()
            print("\nCalculo en modo EXPECTED SARSA")

            # EXPECTEDSARSA
            agentExpectedSarsa = EXPECTEDSARSA(
                calculate_states_size(env),
                env.action_space.n,
                alpha=alp,
                gamma=gam,
                epsilon=eps,
            )
            run(env, agentExpectedSarsa, "epsilon-greedy", episodes, total_rewards_es, array_expecteds, i)
            print("Completado el modo EXPECTED SARSA")
            total_rewards_s, total_rewards_es = totalRewards(n_episodes=episodes)
            i += 1
            env.close()
    printFigureIterable(array_sarsa, seedEps, seedGmm, alp, 0)
    printFigureIterable(array_expecteds, seedEps, seedGmm, alp, 1)
    # printPrueba(total_rewards_s, seedEps, seedGmm, alp, 0)
    # printPrueba(total_rewards_es, seedEps, seedGmm, alp, 1)

def totalRewards(n_episodes):
    total_rewards_s = np.zeros(n_episodes)
    total_rewards_es = np.zeros(n_episodes)
    return total_rewards_s, total_rewards_es


def printFigureIterable(array_imp, seedEps, seedGmm, alp, cond):
    plt.figure(figsize=(12,8))
    iE = 0
    iG = 0

    for i in range(len(array_imp)):
        window = 10
        array_i = array_imp[i]
        s_avg_rewards = np.array([np.mean(array_i[i-window:i])  
                                if i >= window
                                else np.mean(array_i[:i])
                                for i in range(1, len(array_i))
                                ])    
        plt.plot(s_avg_rewards,
                label='E = {} G = {}'.format(seedEps[iE], seedGmm[iG]))
        iG += 1
        if iG == 3:
            iG = 0
            iE += 1

    plt.ylabel('Sum rewards')
    plt.xlabel('Episodes')
    plt.title('Parameters: Env = MountainCar, Alpha  = {}'.format(alp))
    plt.legend()
    if(cond == 0):
        plt.savefig("NEWEnvMountainCarSarsa.jpg", dpi=600)
    else:
        plt.savefig("NEWEnvMountainCarExpectedSarsa.jpg", dpi=600)
    #plt.show()
    

def printFigure(total_alpha_s, total_alpha_es, eps, gam, cond):
    plt.figure(figsize=(10,6))
    plt.plot(total_alpha_s,
            label='Sarsa')
    plt.plot(total_alpha_es,
            label='ExpectedSarsa')
    plt.ylabel('Average return')
    plt.xlabel('Alpha')
    plt.title('Parameters: Env = MountainCar, Epsilon = {}, Gamma = {}'.format(eps, gam))
    plt.legend()
    if cond == 0:
        plt.savefig("NEW-SumEnvMountainCarAlpha.jpg", dpi=600)
    else:
        plt.savefig("NEW-AveEnvMountainCarAlpha.jpg", dpi=600)
    #plt.show()


if __name__ == "__main__":
    episodes = 3000 if len(sys.argv) == 1 else int(sys.argv[1])

    env = gym.make("MountainCar-v0")
    total_rewards_s_train = np.zeros(episodes)
    total_rewards_es_train = np.zeros(episodes)

    total_rewards_s = np.zeros(100)
    total_rewards_es = np.zeros(100)

    total_alpha_s_train = np.zeros(10)
    total_alpha_es_train = np.zeros(10)

    total_alpha_s = np.zeros(10)
    total_alpha_es = np.zeros(10)

    seedAlp = 0.1
    eps = 0.05
    gam = 0.8
    alp = 0.25

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
        run(env, agentSarsa, "epsilon-greedy", episodes, total_rewards_s_train, total_alpha_s_train, i)
        print("Completado el modo SARSA")
        run(env, agentSarsa, "greedy", 100, total_rewards_s, total_alpha_s, i)
        env.reset()
        print("\nCalculo en modo EXPECTED SARSA")
        # EXPECTEDSARSA
        agentExpectedSarsa = EXPECTEDSARSA(
            calculate_states_size(env),
            env.action_space.n,
            alpha=seedAlp,
            gamma=gam,
            epsilon=eps,
        )
        run(env, agentExpectedSarsa, "epsilon-greedy", episodes, total_rewards_es_train, total_alpha_es_train, i)
        print("Completado el modo EXPECTED SARSA\n")
        run(env, agentExpectedSarsa, "greedy", 100, total_rewards_es, total_alpha_es, i)
        total_rewards_s_train, total_rewards_es_train = totalRewards(n_episodes=episodes)
        total_rewards_s, total_rewards_es = totalRewards(n_episodes=100)
        seedAlp += 0.1
    printFigure(total_alpha_s_train, total_alpha_es_train, eps, gam, 0) #sumatoria
    printFigure(total_alpha_s, total_alpha_es, eps, gam, 1) #average
    env.close()
    # Play
    # env = gym.make("MountainCar-v0", render_mode="human")
    # run(env, agent, "greedy", 1)
    # agent.render()
    # env.close()