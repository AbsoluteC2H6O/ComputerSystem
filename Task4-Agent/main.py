import sys
import time
import gym
import gym_environments
import numpy as np
from agentQ import QLearning
from agentDQ import DoubleQLearning

def train(env, agent, episodes, isRandom, max, total_rewards):
    i = 0
    valor = 0
    # while (i < max):
    for _ in range(episodes):
        observation, _ = env.reset()
        terminated, truncated = False, False
        while not (terminated or truncated):
            if(isRandom):
                action = agent.get_action(observation, "random")
            else:
                action = agent.get_action(observation, "epsilon-greedy")
            
            # Count left actions
            # if s_0 == 'A' and action == 1:
            #     left_count_dq[_] += 1
            # s_1, reward, done, _ = env.step(action)

            # Actualization Tables    
            new_observation, reward, terminated, truncated, _ = env.step(action)
            q = agent.update(observation, action, new_observation, reward, terminated)
            # print('q, reward', q, reward)
            observation = new_observation
            if (terminated or truncated):
                valor += reward
            # q1_estimate[ep] += (Q1['A'][env.left] - q1_estimate[ep]) / (ep + 1)
            # q2_estimate[ep] += (Q2['A'][env.left] - q2_estimate[ep]) / (ep + 1)
        total_rewards[i] = valor
        i+=1
    print('total, i', total_rewards, i)

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
    n_episodes = 100
    max_tests = n_episodes*1.2
    
    # Inicialization
    total_rewards = np.zeros(int(n_episodes))
    print('total',total_rewards)
    environments = ["CliffWalking-v0", "Taxi-v3"]
    env = gym.make(environments[1])
    agentQ = QLearning(
        env.observation_space.n, env.action_space.n, alpha=0.1, gamma=0.9, epsilon=0.1
    )
    agentDQ = DoubleQLearning(
        env.observation_space.n, env.action_space.n, alpha=0.1, gamma=0.9, epsilon=0.5
    )
    
    episodes = n_episodes if len(sys.argv) == 1 else int(sys.argv[1])
    # episodes = 100 if len(sys.argv) < 3 else int(sys.argv[2])
    print('')
    train(env, agentQ, episodes+1, True, max_tests, total_rewards)
    env.reset()
    train(env, agentDQ, episodes+1, False, max_tests, total_rewards)
    agentQ.render()
    agentDQ.render()
    env.close()

    # -- Grafica --

    # plt.figure(figsize=(15,8))
    # plt.plot(left_count_q/max_tests*100, 
    #         label='Q-Learning')
    # plt.plot(left_count_dq/max_tests*100, 
    #         label='Double Q-Learning')
    # plt.ylabel('Percentage of Left Actions')
    # plt.xlabel('Episodes')
    # plt.title(r'Q-Learning Action Selection ($\epsilon=0.1$)')
    # plt.legend(loc='best')
    # plt.show()

    # env = gym.make(environments[1], render_mode="human")
    # print("Jugando con Q learning")
    # play(env, agentQ)
    # env.reset()
    # time.sleep(2)
    # print("Jugando con Doble Q learning")
    # play(env, agentDQ)
    # env.close()