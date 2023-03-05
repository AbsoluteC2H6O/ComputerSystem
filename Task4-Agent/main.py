import sys
import time
import gym
import gym_environments
import numpy as np
import matplotlib.pyplot as plt
from agentQ import QLearning
from agentDQ import DoubleQLearning

def train(env, agent, episodes, total_rewards):
    i = 0
    for j in range(episodes):
        if (j % 100  == 0):
            print('Corrida {} de {}'.format(j, episodes))
        observation, _ = env.reset()
        terminated, truncated = False, False
        while not (terminated or truncated):
            # Mode
            action = agent.get_action(observation, "epsilon-greedy")
            # Actualization Tables    
            new_observation, reward, terminated, truncated, _ = env.step(action)
            q = agent.update(observation, action, new_observation, reward, terminated)
            observation = new_observation
            total_rewards[i] += reward
        i+=1

def play(env, agent):
    observation, _ = env.reset()
    env.render()
    terminated, truncated = False, False
    while not (terminated or truncated):
        action = agent.get_action(observation, "greedy")
        new_observation, reward, terminated, truncated, _ = env.step(action)
        agent.update(observation, action, new_observation, reward, terminated)
        observation = new_observation
        env.render()

def totalRewards(n_episodes):
    total_rewards_q = np.zeros(n_episodes)
    total_rewards_dq = np.zeros(n_episodes)
    return total_rewards_q, total_rewards_dq

def printFigure(total_rewards_q, total_rewards_dq, option, gam, alp, seedG, seedA):
    if(option == 0):
        # -- Graph Environment CliffWalking --
        plt.figure(figsize=(10,6))
        plt.plot(total_rewards_q,
                label='Q-Learning')
        plt.plot(total_rewards_dq,
                label='Double Q-Learning')
        plt.ylabel('Sum of rewards during episode')
        plt.xlabel('Episodes')
        plt.title('Parameters: Env = CliffWalking, Epsilon = 0.05, Alpha = {}, Gamma = {}'.format(seedA, seedG))
        plt.legend(loc='lower center', ncol=3, frameon=False)
        plt.savefig("EnvCliffWalkingGamma{}Alpha{}.jpg".format(gam, alp), dpi=600)
        #plt.show()
    else:
        # -- Graph Taxi --
        window = 20
        q_avg_rewards = np.array([np.mean(total_rewards_q[i-window:i])  
                                if i >= window
                                else np.mean(total_rewards_q[:i])
                                for i in range(1, len(total_rewards_q))
                                ])
        dq_avg_rewards = np.array([np.mean(total_rewards_dq[i-window:i])  
                                if i >= window
                                else np.mean(total_rewards_dq[:i])
                                for i in range(1, len(total_rewards_dq))
                                ])
        plt.figure(figsize=(10,6))
        plt.plot(q_avg_rewards,
                label='Q-Learning')
        plt.plot(dq_avg_rewards,
                label='Double Q-Learning')
        plt.ylabel('Sum of rewards during episode')
        plt.xlabel('Episodes')
        plt.title('Parameters: Env = Taxi, Epsilon = 0.05, Alpha = {}, Gamma = {}'.format(seedA, seedG))
        plt.legend(loc='lower center', ncol=3, frameon=False)
        plt.savefig("EnvCliffWalkingGamma{}Alpha{}.jpg".format(gam, alp), dpi=600)
        #plt.show()

if __name__ == "__main__":
    # Iterators
    n_epis = 500
    seedGam, seedAlp = 0.1, 0.05
    # Type environment: 0 = CliffWalking, 1 = Taxi
    option = - 1
    # Inicialization
    eps = 0.05
    total_rewards_q = np.zeros(n_epis)
    total_rewards_dq = np.zeros(n_epis)
    environments = ["CliffWalking-v0", "Taxi-v3"]
    
    print('Hola! Elije el Env a ejecutar: 0 = CliffWalking o 1 = Taxi.')
    while(option != 0 and option !=1):
        option = int(input())
        if(option < 0 or option > 1):
            print('Opcion incorrecta, marque una opcion entre 0 o 1.')

    env = gym.make(environments[option])
    # agentQ = QLearning(
    #     env.observation_space.n, env.action_space.n, alpha=seedAlp, gamma=seedGam, epsilon=eps
    # )
    # agentDQ = DoubleQLearning(
    #     env.observation_space.n, env.action_space.n, alpha=seedAlp, gamma=seedGam, epsilon=eps
    # )
    episodes = n_epis if len(sys.argv) == 1 else int(sys.argv[1])
    print('Environment elegido: {}'.format(environments[option]))
    time.sleep(0.5)
    for i in range(3):
        for j in range(10):
            print('Parametros: Epsilon = {}, Gamma = {}, Alpha = {}'.format(eps, seedGam, seedAlp))
            agentQ = QLearning(
                env.observation_space.n, env.action_space.n, alpha=seedAlp, gamma=seedGam, epsilon=eps
            )
            agentDQ = DoubleQLearning(
                env.observation_space.n, env.action_space.n, alpha=seedAlp, gamma=seedGam, epsilon=eps
            )
            # Q-Learning
            print('Calculo en modo Q-Learning')
            train(env, agentQ, episodes, total_rewards_q)
            print('Completado modo Q-Learning')
            env.reset()
            # Doble Q-Learning
            print('\nCalculo en modo Doble Q-Learning')
            train(env, agentDQ, episodes, total_rewards_dq)
            print('Completado modo Doble Q-Learning')
            agentQ.render()
            agentDQ.render()
            printFigure(total_rewards_q, total_rewards_dq, option, i+1, j+1, seedG=seedGam, seedA=seedAlp)
            totalRewards(n_episodes=n_epis)
            seedAlp += 0.1
        seedGam += 0.35
    env.close()

    # env = gym.make(environments[1], render_mode="human")
    # print("Jugando con Q learning")
    # play(env, agentQ)
    # env.reset()
    # time.sleep(2)
    # print("Jugando con Doble Q learning")
    # play(env, agentDQ)
    # env.close()