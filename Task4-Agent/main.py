import sys
import time
import gym
import gym_environments
from agentQ import QLearning
from agentDQ import DoubleQLearning

def train(env, agent, episodes, isRandom):
    for _ in range(episodes):
        observation, _ = env.reset()
        terminated, truncated = False, False
        while not (terminated or truncated):
            if(isRandom):
                action = agent.get_action(observation, "random")
            else:
                action = agent.get_action(observation, "epsilon-greedy")
            new_observation, reward, terminated, truncated, _ = env.step(action)
            agent.update(observation, action, new_observation, reward, terminated)
            observation = new_observation

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
    environments = ["CliffWalking-v0", "Taxi-v3"]
    env = gym.make(environments[1])
    agentQ = QLearning(
        env.observation_space.n, env.action_space.n, alpha=0.1, gamma=0.9, epsilon=0.1
    )
    agentDQ = DoubleQLearning(
        env.observation_space.n, env.action_space.n, alpha=0.1, gamma=0.9, epsilon=0.5
    )
    
    episodes = 5000 if len(sys.argv) == 1 else int(sys.argv[1])
    # episodes = 100 if len(sys.argv) < 3 else int(sys.argv[2])
    print('')
    train(env, agentQ, episodes, True)
    env.reset()
    train(env, agentDQ, episodes, False)
    agentQ.render()
    agentDQ.render()
    env.close()

    env = gym.make(environments[1], render_mode="human")
    print("Jugando con Q learning")
    play(env, agentQ)
    env.reset()
    time.sleep(2)
    print("Jugando con Doble Q learning")
    play(env, agentDQ)
    env.close()
