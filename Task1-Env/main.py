#importar modulos
import sys #lista de directorios/carpetas
import gym #standard API
import gym_environments #entorno para nuestro agente
from agent import TwoArmedBandit #importamos nuestra agente

num_iterations = 100 if len(sys.argv) < 2 else int(sys.argv[1])
version = "v1" if len(sys.argv) < 3 else sys.argv[2]

env = gym.make(f"TwoArmedBandit-{version}") #entorno
agent = TwoArmedBandit(0.1, 0.5) #valores de alpha y epsilon

env.reset(options={'delay': 1}) #resetear el entorno

for iteration in range(num_iterations):
    action = agent.get_action("random")    
    _, reward, _, _, _ = env.step(action)
    agent.update(action, reward) 
    agent.render()

env.close() #cierre del entorno
