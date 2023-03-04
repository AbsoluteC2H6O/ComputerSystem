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
            time.sleep(0.5)
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

def totalRewards():
    total_rewards_q = np.zeros(n_episodes)
    total_rewards_dq = np.zeros(n_episodes)
    return total_rewards_q, total_rewards_dq


def play(env, agent):
    observation, _ = env.reset()
    env.render()
    time.sleep(1)
    terminated, truncated = False, False
    while not (terminated or truncated):
        action = agent.get_action(observation, "greedy")
        new_observation, reward, terminated, truncated, _ = env.step(action)
        agent.update(observation, action, new_observation, reward, terminated)
        observation = new_observation
        env.render()


if __name__ == "__main__":
    # Iterators
    n_episodes = 50
    # Type environment: 0 = CliffWalking, 1 = Taxi
    option = 0
    # Inicialization
    total_rewards_q = np.zeros(n_episodes)
    total_rewards_dq = np.zeros(n_episodes)
    # total_rewards_q1 = np.zeros(n_episodes)
    # total_rewards_dq1 = np.zeros(n_episodes)

    environments = ["CliffWalking-v0", "Taxi-v3"]
    env = gym.make(environments[option])
    #env1 = gym.make(environments[option+1])
    agentQ = QLearning(
        env.observation_space.n, env.action_space.n, alpha=0.1, gamma=0.9, epsilon=0.05
    )
    agentDQ = DoubleQLearning(
        env.observation_space.n, env.action_space.n, alpha=0.1, gamma=0.9, epsilon=0.05
    )
    # agentQ1 = QLearning(
    #     env.observation_space.n, env.action_space.n, alpha=0.1, gamma=0.9, epsilon=0.05
    # )
    # agentDQ1 = DoubleQLearning(
    #     env.observation_space.n, env.action_space.n, alpha=0.1, gamma=0.9, epsilon=0.05
    # )
    
    episodes = n_episodes if len(sys.argv) == 1 else int(sys.argv[1])
    # Q-Learning
    print('Calculo en modo Q-Learning')
    time.sleep(1)
    train(env, agentQ, episodes, total_rewards_q)
    print('Completado modo Q-Learning')
    env.reset()
    # Doble Q-Learning
    time.sleep(1)
    print('\nCalculo en modo Doble Q-Learning')
    train(env, agentDQ, episodes, total_rewards_dq)
    print('Completado modo Doble Q-Learning')
    agentQ.render()
    agentDQ.render()
    #env.close()

    # # Q-Learning
    # print('Calculo en modo Q-Learning')
    # time.sleep(1)
    # train(env1, agentQ1, episodes, total_rewards_q1)
    # print('Completado modo Q-Learning')
    # env1.reset()
    # # Doble Q-Learning
    # time.sleep(1)
    # print('\nCalculo en modo Doble Q-Learning')
    # train(env1, agentDQ1, episodes, total_rewards_dq1)
    # print('Completado modo Doble Q-Learning')
    # agentQ.render()
    # agentDQ.render()
    # env.close()
    # env1.close()

    if(option == 0):
        # -- Graph Environment CliffWalking --
        # plt.figure(figsize=(8,4))
        # plt.subplot(2, 1, 1) 
        # plt.plot(total_rewards_q, label='Q-Learning')
        # plt.title(r'Individual Graphs. Env = CliffWalking.')
        # plt.legend()

        # #plt.figure(figsize=(8,4))
        # plt.subplot(2, 1, 2)
        # plt.plot(total_rewards_dq, label='Double Q-Learning', color ='orange')
        # plt.legend()
        # plt.show()

        plt.figure(figsize=(10,6))
        plt.plot(total_rewards_q,
                label='Q-Learning')
        plt.plot(total_rewards_dq,
                label='Double Q-Learning')
        # plt.hlines(xmin=0, xmax=episodes, y=0.05/6*100, 
        #     label='Optimal')
        plt.ylabel('Sum of rewards during episode')
        plt.xlabel('Episodes')
        plt.title(r'Parameters: Env = CliffWalking, ($\epsilon = 0.05$), ($\alpha = 0.1$), ($\gamma = 0.9$)')
        plt.legend()
        plt.savefig("figura_base{}.jpg".format(10), dpi=600)
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
                
        # plt.figure(figsize=(8,4))
        # plt.subplot(2, 1, 1) 
        # plt.plot(q_avg_rewards, label='Q-Learning')
        # plt.title(r'Individual Graphs. Env = Taxi.')
        # plt.legend()

        # plt.subplot(2, 1, 2)
        # plt.plot(dq_avg_rewards, label='Double Q-Learning', color ='orange')
        # plt.legend()
        # plt.show()

        plt.figure(figsize=(10,6))
        plt.plot(q_avg_rewards,
                label='Q-Learning')
        plt.plot(dq_avg_rewards,
                label='Double Q-Learning')
        # plt.hlines(xmin=0, xmax=episodes, y=0.05/6*100, 
        #     label='Optimal')
        plt.ylabel('Sum of rewards during episode')
        plt.xlabel('Episodes')
        plt.title(r'Parameters: Env = Taxi, ($\epsilon = 0.05$), ($\alpha = 0.1$), ($\gamma = 0.9$)')
        plt.legend(loc='lower center', ncol=3, frameon=False)
        plt.savefig("figura_base{}.jpg".format(11), dpi=600)
        #plt.show()

    # env = gym.make(environments[1], render_mode="human")
    # print("Jugando con Q learning")
    # play(env, agentQ)
    # env.reset()
    # time.sleep(2)
    # print("Jugando con Doble Q learning")
    # play(env, agentDQ)
    # env.close()