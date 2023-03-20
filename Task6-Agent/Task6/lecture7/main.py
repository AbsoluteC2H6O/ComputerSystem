import sys
import gym
import gym_environments
import numpy as np
import matplotlib.pyplot as plt
from agentDynaQ import agentDynaQ
from agentDynaQPlus import agentDynaQPlus


def run(env, agent, selection_method, episodes):
    step = 0
    total_steps = np.zeros(episodes)
    for episode in range(episodes):
        observation, _ = env.reset()
        if (episode % 100 == 0):
            print("Episode", episode)
        agent.start_episode()
        terminated, truncated = False, False
        while not (terminated or truncated):
            action = agent.get_action(observation, selection_method)
            next_observation, reward, terminated, truncated, _ = env.step(
                action)
            agent.update(observation, action, next_observation, reward)
            observation = next_observation
        if selection_method == "epsilon-greedy":
            for _ in range(100):
                state = np.random.choice(list(agent.visited_states.keys()))
                action = np.random.choice(agent.visited_states[state])
                reward, next_state = agent.model[(state, action)]
                step = agent.update(state, action, next_state, reward)
        total_steps[episode]+=step
        step = 0
    return total_steps

def printFigureIterable(array_dyna, array_dyna_plus):
    plt.figure(figsize=(12, 8))
    plt.plot(array_dyna,
             label='Dyna Q')
    plt.plot(array_dyna_plus,
             label='Dyna Q +')

    plt.ylabel('Steps per episodes- Training')
    plt.xlabel('Episodes')
    plt.title(label='E = {} G = {} A={}'.format(0.1, 0.95, 1))
    plt.legend()
    plt.savefig("BlockEnvironmentDynaQvsDynaQPlus-Training.jpg", dpi=600)


if __name__ == "__main__":
    environments = ["Princess-v0", "Blocks-v0"]
    id = 1 if len(sys.argv) < 2 else int(sys.argv[1])
    episodes = 1000 if len(sys.argv) < 3 else int(sys.argv[2])

    steps_dyna_q = np.zeros(episodes)
    steps_dyna_q_plus = np.zeros(episodes)

# Dyna Q
    env = gym.make(environments[id])
    agent = agentDynaQ(
        env.observation_space.n, env.action_space.n, alpha=1, gamma=0.95, epsilon=0.1
    )
    # Train
    totals_q = np.zeros(episodes)
    for i in range(2):
        dyna_q_train = run(env, agent, "epsilon-greedy", episodes)
        for i in range(episodes):
            totals_q[i]+= dyna_q_train[i]
    for i in range(episodes):
        totals_q[i]= totals_q[i]/2

# Dyna Q +
    env.reset()
    agent = agentDynaQPlus(
        env.observation_space.n, env.action_space.n, alpha=1, gamma=0.95, epsilon=0.1
    )
    # Train
    totals_q_plus = np.zeros(episodes)
    for i in range(2):
        dyna_q_plus_train = run(env, agent, "epsilon-greedy", episodes)
        for i in range(episodes):
            totals_q_plus[i]+= dyna_q_plus_train[i]
    for i in range(episodes):
        totals_q_plus[i]= totals_q_plus[i]/2
    
    # grafica steps per episode vs Episodes.
    printFigureIterable(totals_q, totals_q_plus)
    env.close()
