
import os
import time
from frozen_lake import RobotBatteryEnv
# from agent import ValueIteration
# Allowing environment to have sounds
if "SDL_AUDIODRIVER" in os.environ:
    del os.environ["SDL_AUDIODRIVER"]
    
env = RobotBatteryEnv(rows=16, cols=16,render_mode="human")
env.render()

env.renderPygame()
# agent = ValueIteration(env.observation_space.n, env.action_space.n, env.P, 0.9)
# agent.solve(1000)
# agent.render()

# observation, info = env.reset()
# terminated, truncated = False, False

# env.render()
# time.sleep(1)

# while not (terminated or truncated):
#     action = agent.get_action(observation)
#     observation, _, terminated, truncated, _ = env.step(action)

# time.sleep(1)
# env.close()