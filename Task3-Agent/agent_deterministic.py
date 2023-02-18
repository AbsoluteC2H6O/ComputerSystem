import numpy as np

class MonteCarloDet:
    def __init__(self, states_n, actions_n, gamma, epsilon):
        self.states_n = states_n
        self.actions_n = actions_n
        self.gamma = gamma
        self.epsilon = epsilon
        self.reset()

    def reset(self):
        self.episode = [] # número de episodios
        self.q = np.zeros((self.states_n, self.actions_n)) # valorar cada par estado-acción
        # self.pi = np.zeros(self.states_n, , self.actions_n) # recibe un estado y retorna una acción, determina que acción seguir
        self.pi = np.full((self.states_n, self.actions_n), 1 / self.actions_n)
        self.returns = np.full((self.states_n, self.actions_n), 0) # Acumular los promedios
        self.returns_n = np.zeros((self.states_n, self.actions_n)) # acumula el numero de iter

    def update(self, state, action, reward, terminated):
        self.episode.append((state, action, reward))
        if terminated == True:
            self._update_q()
            # self._update_pi()
            self.episode = [] # inicializo de nuevo los episodios

    def _update_q(self):       
        G = 0
        #print('episode', self.episode)
        self.episode.reverse()
        states_actions = []
        [
            states_actions.append((state, action))
            for state, action, _ in self.episode
            if (state, action) not in states_actions
        ]
        #print('reverse', self.episode)
        reward = self.episode[0][2]
        for state, action, reward_a in self.episode[1:]:
            # first_occurence = next(
            #     i
            #     for i, step in enumerate(self.episode)
            #     if step[0] == state and step[1] == action
            # )
            # print('first:',first_occurence)
            G = self.gamma*G + reward
            reward = reward_a
            print('G', G)
            if (state, action) in states_actions:
                self.returns[state][action] = G
                self.returns_n[state][action] = np.average(self.returns[state][action])
                self.q[state][action] = self.returns_n[state][action]
                self.pi[state] = np.argmax(self.q[state])
            #self.pi = np.argmax(self.q[state])  
        #     print('returns', self.returns[state][action])
        # print('returns total', self.returns)
        # print('q total', self.q)

    # def _update_pi(self):
    #     states = []
    #     [states.append(state) for state, _, _ in self.episode if state in states]
    #     for state in states:
    #         best_action = np.argmax(self.q[state])
    #         self.pi[state] = best_action
    
    def get_action(self, state):
        print(self.pi[state])
        return np.random.choice(self.actions_n, p=self.pi[state])

    def get_best_action(self, state):
        return np.argmax(self.q[state])

    def render(self):
        print(f"Values: {self.q}\nPolicy: {self.pi}")