import sys
import gym
import gym_environments
import numpy as np
import matplotlib.pyplot as plt
from agentDynaQ import agentDynaQ
from agentDynaQPlus import agentDynaQPlus


def run(env, agent, selection_method, episodes):
    step = 0
    total_steps = []
    total_average= []
    for _ in range(10):
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
            total_steps.append(step)
            step = 0
        total_average.append(total_steps[episode])
    return total_average

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
    id = 0 if len(sys.argv) < 2 else int(sys.argv[1])
    episodes = 350 if len(sys.argv) < 3 else int(sys.argv[2])

    steps_dyna_q = np.zeros(episodes)
    steps_dyna_q_plus = np.zeros(episodes)

# Dyna Q
    env = gym.make(environments[id])
    agent = agentDynaQ(
        env.observation_space.n, env.action_space.n, alpha=1, gamma=0.95, epsilon=0.1
    )
    # Train
    dyna_q_train = run(env, agent, "epsilon-greedy", episodes)

# Dyna Q +
    env.reset()
    agent = agentDynaQPlus(
        env.observation_space.n, env.action_space.n, alpha=1, gamma=0.95, epsilon=0.1
    )
    # Train
    dyna_q_plus_train = run(env, agent, "epsilon-greedy", episodes)
    # grafica steps per episode vs Episodes.
    printFigureIterable(dyna_q_train, dyna_q_plus_train)
    env.close()
