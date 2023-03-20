import sys
import gym
import gym_environments
import numpy as np
import matplotlib.pyplot as plt
from agentDynaQ import agentDynaQ
from agentDynaQPlus import agentDynaQPlus

def run(env, agent: agentDynaQ, selection_method, episodes):
    steps =0
    step = 0
    total_average = []
    for episode in range(episodes):
        if episode > 0:
            print(f"Episode: {episode+1}")
        observation, _ = env.reset()
        agent.start_episode()
        terminated, truncated = False, False
        while not (terminated or truncated):
            steps+=1
            action = agent.get_action(observation, selection_method)
            next_observation, reward, terminated, truncated, _ = env.step(action)
            agent.update(observation, action, next_observation, reward)
            observation = next_observation
        if selection_method == "epsilon-greedy":
            for _ in range(100):
                state = np.random.choice(list(agent.visited_states.keys()))
                action = np.random.choice(agent.visited_states[state])
                reward, next_state = agent.model[(state, action)]
                step = agent.update(state, action, next_state, reward)
        total_average.append(step)
        step=0
    return total_average
    
                
def printFigureIterable(array_dyna, array_dyna_plus):
    plt.figure(figsize=(12,8))
    plt.plot(array_dyna,
                label='Dyna Q')
    plt.plot(array_dyna_plus,
                label='Dyna Q +')

    plt.ylabel('Steps per episodes')
    plt.xlabel('Episodes')
    plt.title(label='E = {} G = {} A='.format(0.1,0.95,1))
    plt.legend()
    plt.savefig("BlockEnvironmentDynaQvsDynaQPlus.jpg", dpi=600)

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
    steps_dyna_q = run(env, agent, "epsilon-greedy", episodes)
    env.close()

    # Play
    # env = gym.make(environments[id], render_mode="human")
    # run(env, agent, "greedy", 1)
    # agent.render()
    # grafica steps per episode vs Episodes.
    
# Dyna Q + 
    env = gym.make(environments[id])
    agent = agentDynaQPlus(
        env.observation_space.n, env.action_space.n, alpha=1, gamma=0.95, epsilon=0.1
    )

    # Train
    steps_dyna_q_plus=run(env, agent, "epsilon-greedy", episodes)
    env.close()

    # Play
    # env = gym.make(environments[id], render_mode="human")
    # run(env, agent, "greedy", 1)
    # agent.render()
    printFigureIterable(steps_dyna_q,steps_dyna_q_plus)
    # grafica steps per episode vs Episodes.
    env.close()