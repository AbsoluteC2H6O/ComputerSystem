
from agentSarsaE import EXPECTEDSARSA
from agentSarsa  import SARSA
import matplotlib.pyplot as plt
import gym_environments
import numpy as np
import time
import sys
import gym

def calculate_states_size(env):
    max = env.observation_space.high
    min = env.observation_space.low
    sizes = (max - min) * np.array([10, 100]) + 1
    return int(sizes[0]) * int(sizes[1])


def calculate_state(env, value):
    min = env.observation_space.low
    values = (value - min) * np.array([10, 100])
    return int(values[1]) * 19 + int(values[0])


def run(env, agent, selection_method, episodes):
    i = 0
    total_rewards = np.zeros(episodes)
    for episode in range(1, episodes + 1):
        # if episode % 100 == 0:
        #     print(f"Episode: {episode}")
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
        i+=1
    return total_rewards

def totalRewards(n_episodes):
    total_rewards_q = np.zeros(n_episodes)
    total_rewards_dq = np.zeros(n_episodes)
    return total_rewards_q, total_rewards_dq

def printFigure(total_rewards_s, total_rewards_es, alp, eps, seedA, seedE):
    # -- Graph Environment MountainCar --
    window = 80
    for j in range(len(total_rewards_s)-1):
        totals_sarsa = total_rewards_s[j]
        totals_esarsa = total_rewards_es[j]
        s_avg_rewards = np.array([np.mean(totals_sarsa[i-window:i])  
                                if i >= window
                                else np.mean(totals_sarsa[:i])
                                for i in range(1, len(totals_sarsa))
                                ])
        es_avg_rewards = np.array([np.mean(totals_esarsa[i-window:i])  
                                if i >= window
                                else np.mean(totals_esarsa[:i])
                                for i in range(1, len(totals_esarsa))
                                ])
        plt.figure(figsize=(10,6))
        plt.plot(s_avg_rewards,
                label='Sarsa')
        plt.plot(es_avg_rewards,
                label='ExpectedSarsa')
        plt.ylabel('Sum of rewards during episode')
        plt.xlabel('Episodes')
        plt.title('Parameters: Env = MountainCar, Gamma = 0.95, Alpha = {}, Epsilon = {}'.format(seedA, seedE))
        plt.legend(ncol=2)
        plt.savefig("EnvMountainCarEps{}Alpha{}.jpg".format(eps, alp), dpi=600)

if __name__ == "__main__":
    episodes = 40 if len(sys.argv) == 1 else int(sys.argv[1])

    env = gym.make("MountainCar-v0")
    total_rewards_sarsa = np.zeros(episodes)
    total_rewards_sarsa_e = np.zeros(episodes)
    totals_rewards_sarsa = []
    totals_rewards_sarsa_e = []
    seedGam, seedAlp, seedEps = 0.95, 0.2, 0.05
    it = 0
    for i in range(3):
        seedAlp = 0.2
        for j in range(3):
            print('\nParametros: Epsilon = {}, Gamma = {}, Alpha = {}'.format(seedEps, seedGam, seedAlp))
        #SARSA
            print('SARSA RUN')
            agentS = SARSA(
                calculate_states_size(env),
                env.action_space.n,
                alpha=seedAlp,
                gamma=seedGam,
                epsilon=seedEps,
            )
            # Train
            total_rewards_sarsa = run(env, agentS, "epsilon-greedy", episodes)
            # env.close()

            # Play
            # env = gym.make("MountainCar-v0", render_mode="human")
            # run(env, agentS, "greedy", 1)
            # agentS.render()
            # env.close()
            
            time.sleep(1)
        # Expected Sarsa
            # env = gym.make("MountainCar-v0")
            env.reset()
            agentE = EXPECTEDSARSA(
                calculate_states_size(env),
                env.action_space.n,
                alpha=seedAlp,
                gamma=seedGam,
                epsilon=seedEps,
            )
            print('EXPECTED SARSA RUN\n')
            # Train
            total_rewards_sarsa_e = run(env, agentE, "epsilon-greedy", episodes)
            env.close()

            # Play
            # env = gym.make("MountainCar-v0", render_mode="human")
            # run(env, agentE, "greedy", 1)
            # agentE.render()
            # env.close()
            totals_rewards_sarsa.insert(it, total_rewards_sarsa)
            totals_rewards_sarsa_e.insert(it, total_rewards_sarsa_e)
            total_rewards_q, total_rewards_dq = totalRewards(n_episodes=episodes)
            seedAlp += 0.3
            it += 1
        seedEps += 0.3
    
    printFigure(totals_rewards_sarsa, totals_rewards_sarsa_e, i+1, j+1, seedA=seedAlp, seedE=seedEps)