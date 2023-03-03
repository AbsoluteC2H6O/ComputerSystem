import sys
import time
import gym
import gym_environments
import numpy as np
import matplotlib.pyplot as plt
from agentQ import QLearning
from agentDQ import DoubleQLearning

def train(env, agent, episodes, isRandom, max, total_rewards):
    i = 0
    #while (i < max):
    valor = 0
    for j in range(episodes):
        observation, _ = env.reset()
        terminated, truncated = False, False
        while not (terminated or truncated):
            if(isRandom):
                action = agent.get_action(observation, "greedy")
            else:
                action = agent.get_action(observation, "epsilon-greedy")

            # Actualization Tables    
            new_observation, reward, terminated, truncated, _ = env.step(action)
            q = agent.update(observation, action, new_observation, reward, terminated)
            # print('q, reward', q, reward)
            observation = new_observation
            # if(terminated or truncated):
            total_rewards[i] += reward
                #print('# episode, valor, reward', j, valor, reward)
            # q1_estimate[ep] += (Q1['A'][env.left] - q1_estimate[ep]) / (ep + 1)
            # q2_estimate[ep] += (Q2['A'][env.left] - q2_estimate[ep]) / (ep + 1)
        #total_rewards[i] = valor
        i+=1
    print('total', total_rewards)

def play(env, agent):
    observation, _ = env.reset()
    env.render()
    time.sleep(2)
    terminated, truncated = False, False
    while not (terminated or truncated):
        action = agent.get_action(observation, "greedy")
        new_observation, reward, terminated, truncated, _ = env.step(action)
        agent.update(observation, action, new_observation, reward, terminated)
        observation = new_observation
        env.render()


if __name__ == "__main__":
    # Iterators
    n_episodes = 10000
    max_tests = 10
    print('Cantidad de episodios: {}. Cantidad de tests: {}. '
          'Cantidad total por tipo de Qlearning: {}'.format(n_episodes, max_tests, n_episodes*max_tests))
    # Inicialization
    total_rewards_q = np.zeros(n_episodes)
    total_rewards_dq = np.zeros(n_episodes)
    environments = ["CliffWalking-v0", "Taxi-v3"]
    env = gym.make(environments[1])
    agentQ = QLearning(
        env.observation_space.n, env.action_space.n, alpha=0.1, gamma=0.9, epsilon=0.5
    )
    agentDQ = DoubleQLearning(
        env.observation_space.n, env.action_space.n, alpha=0.1, gamma=0.9, epsilon=0.5
    )
    
    episodes = n_episodes if len(sys.argv) == 1 else int(sys.argv[1])
    print('')
    # Q-Learning
    train(env, agentQ, episodes, False, max_tests, total_rewards_q)
    env.reset()
    # Doble Q-Learning
    train(env, agentDQ, episodes, False, max_tests, total_rewards_dq)
    agentQ.render()
    agentDQ.render()
    env.close()

    # -- Grafica --

    window = 100
    dq_avg_rewards = np.array([np.mean(total_rewards_dq[i-window:i])  
                            if i >= window
                            else np.mean(total_rewards_dq[:i])
                            for i in range(1, len(total_rewards_dq))
                            ])
    q_avg_rewards = np.array([np.mean(total_rewards_q[i-window:i])  
                            if i >= window
                            else np.mean(total_rewards_q[:i])
                            for i in range(1, len(total_rewards_q))
                            ])

    plt.figure(figsize=(10,6))
    plt.plot(q_avg_rewards,
            label='Q-Learning')
    plt.plot(dq_avg_rewards,
            label='Double Q-Learning')
    plt.hlines(xmin=0, xmax=episodes, y=0.5/6*100, 
           label='Optimal')
    plt.ylabel('Sum of rewards during episode')
    plt.xlabel('Episodes')
    plt.title(r'Q-Learning Action Selection ($\epsilon=0.5$)')
    plt.legend()
    plt.show()

    # env = gym.make(environments[1], render_mode="human")
    # print("Jugando con Q learning")
    # play(env, agentQ)
    # env.reset()
    # time.sleep(2)
    # print("Jugando con Doble Q learning")
    # play(env, agentDQ)
    # env.close()