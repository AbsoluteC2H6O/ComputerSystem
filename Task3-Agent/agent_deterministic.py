import numpy as np


class MonteCarloDet:
    def __init__(self, states_n, actions_n, gamma):
        self.states_n = states_n
        self.actions_n = actions_n
        self.gamma = gamma
        self.reset()

    def reset(self):
        self.episode = []  # número de episodios
        # valorar cada par estado-acción
        self.q = np.zeros((self.states_n, self.actions_n))
        self.pi = np.zeros((self.states_n))
        # Acumular los promedios
        self.returns = np.zeros((self.states_n, self.actions_n))
        # acumula el numero de iter
        self.returns_n = np.zeros((self.states_n, self.actions_n))

    def update(self, state, action, reward, terminated):
        self.episode.append((state, action, reward))
        if terminated == True:
            self._update_q()
            self.episode = []  # inicializo de nuevo los episodios

    def _update_q(self):
        G = 0
        self.episode.reverse()
        states_actions = []
        [
            states_actions.append((state, action, reward))
            for state, action, reward in self.episode
            if (state, action, reward) not in states_actions
        ]
        reward = self.episode[0][2]
        state_t= self.episode[0][0]
        action_t = self.episode[0][1]
        for state, action, reward_a in self.episode[0:]:
            G = self.gamma*G + reward
            self.returns_n[state][action] += 1
            if (state_t, action_t, reward) in states_actions[0:len(states_actions)-1]:
                self.returns[state_t][action_t] = G
                # self.returns_n[state_t][action_t] = np.average(
                #     self.returns[state_t][action_t])
                self.q[state_t][action_t] =np.average(
                    self.returns[state_t][action_t])
                self.pi[state_t]= np.argmax(self.q[state_t][action])
                print('self.q', self.q)
                # print('self.pi', self.pi)
            reward = reward_a
            state_t = state
            action_t = action
                
    def get_action(self, state):
        return np.random.choice(self.actions_n)
    
    def get_action_greedy(self, state):
        return np.argmax(self.actions_n)
    
    def get_best_action(self, state):
        return np.argmax(self.q[state])

    def render(self):
        print(f"Values: {self.q}\n")
