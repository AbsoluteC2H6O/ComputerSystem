#importar modulos
import sys #lista de directorios/carpetas
import gym #standard API
import gym_environments #entorno para nuestro agente
from agent import TwoArmedBandit #importamos nuestra agente

num_iterations = 100 if len(sys.argv) < 2 else int(sys.argv[1])
version = "v0" if len(sys.argv) < 3 else sys.argv[2]

env = gym.make(f"TwoArmedBandit-{version}") #entorno
agent = TwoArmedBandit(0.1, 0.9) #agente

env.reset(options={'delay': 1}) #resetear el entorno

print("\nEjecutando el modo: Random", end="\n\n")
for iteration in range(num_iterations):
    action = agent.get_action("random") #elegir el caso de estudio: random, greedy, epsilon
    _, reward, _, _, _ = env.step(action) #obtener la recompensa
    agent.update(action, reward) #actualizar
    agent.render() #nos sirve para ver la evolucion en la tabla de valores e imprimir por pantalla
agent.renderRewardTotal()

env.reset(options={'delay': 1})
agent.reset()
print("\nEjecutando el modo: Greedy", end="\n\n")

for iteration in range(num_iterations):
    action = agent.get_action("greedy")
    _, reward, _, _, _ = env.step(action)
    agent.update(action, reward)
    agent.render()
agent.renderRewardTotal()

env.reset(options={'delay': 1})
agent.reset()
print("\nEjecutando el modo: Epsilon", end="\n\n")

for iteration in range(num_iterations):
    action = agent.get_action("epsilon")
    _, reward, _, _, _ = env.step(action)
    agent.update(action, reward)
    agent.render()
agent.renderRewardTotal()

env.close() #cierre del entorno