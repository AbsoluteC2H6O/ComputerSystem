#importar modulos
import sys #lista de directorios/carpetas
import gym #standard API
import gym_environments #entorno para nuestro agente
from agent import TwoArmedBandit #importamos nuestra agente

num_iterations = 100 if len(sys.argv) < 2 else int(sys.argv[1])
version = "v0" if len(sys.argv) < 3 else sys.argv[2]
num_methods = 3

env = gym.make(f"TwoArmedBandit-{version}") #entorno
agent = TwoArmedBandit(0.1, 0.5) #valores de alpha y epsilon

env.reset(options={'delay': 1}) #resetear el entorno

def executeMethods(method, num_iterations):
    print("\nEjecutando el modo: {}".format(method), end="\n\n")
    for iteration in range(num_iterations):
        action = agent.get_action(method) #elegir el caso de estudio: random, greedy, epsilon
        _, reward, _, _, _ = env.step(action) #obtener la recompensa
        agent.update(action, reward) #actualizar
        agent.render() #nos sirve para ver la evolucion en la tabla de valores e imprimir por pantalla
    agent.renderRewardTotal() #para conocer la ganancia total obtenida
    agent.reset()

for method_number in range(num_methods):
    method = ''
    if method_number == 0:
        method ='random'
    if method_number == 1:
        method ='greedy'
    if method_number == 2:
        method ='epsilon'
    executeMethods(method,num_iterations)
env.close() #cierre del entorno
