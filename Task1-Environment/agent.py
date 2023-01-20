import numpy as np #importamos la lib de objetos de matrices multidimensionales
class TwoArmedBandit(): #creamos nuestra clase TwoArmedBandit

    #iniciar variables: # de bandits = 2, alpha y reset para limpiar las variables
    def __init__(self, alpha=1, eps=0.5):
        self.arms = 2 #numero de bandits
        self.alpha = alpha #valor de alpha
        self.eps = eps #valor de epsilon
        self.reset() #resetear

    #reiniciar las variables y condiciones
    def reset(self):
        self.action = 0 #accion
        self.reward = 0 #recompensa
        self.iteration = 0 #tasa de aprendizaje
        self.values = np.zeros(self.arms)
        self.rewards = np.zeros(self.arms)

    #valorar las acciones
    def update(self, action, reward):
        self.action = action
        self.reward = reward
        self.rewards[action] += reward
        self.iteration += 1
        self.values[action] = self.values[action] + self.alpha * (reward - self.values[action])

    #decidir que accion tomar
    def get_action(self, mode):
        if mode == 'random':
            return np.random.choice(self.arms)
        elif mode == 'greedy':
            return np.argmax(self.values)
        elif mode == 'epsilon':
            p = np.random.random()
            if p < self.eps:
                return np.random.choice(self.arms)
            else:
                return np.argmax(self.values)

    #renderizar
    def render(self):
        print("Iteration: {}, Action: {}, Reward Actual: {}, Values: {}".format(
            self.iteration, self.action, self.reward, self.values))

    #renderizar rewards
    def renderRewardTotal(self):
        print("\nRewards Total: {}".format(
            self.rewards[0]  + self.rewards[1]))
