import numpy as np


class MonteCarloDet:
    def __init__(self, states_n, actions_n, gamma):
        self.states_n = states_n
        self.actions_n = actions_n
        self.gamma = gamma
        self.pi = np.full((self.states_n, self.actions_n), 1 / self.actions_n)
        self.reset()

    def reset(self):
        self.episode = []  # número de episodios
        # valorar cada par estado-acción
        self.q = np.zeros((self.states_n, self.actions_n))
        self.pi = np.full((self.states_n, self.actions_n), 1 / self.actions_n)
        # Acumular los promedios
        self.returns = np.zeros((self.states_n, self.actions_n))
        # acumula el numero de iter
        self.returns_n = np.zeros((self.states_n, self.actions_n))

    def update(self, state, action, reward, terminated):
        self.episode.append((state, action, reward))
        if terminated == True:
            self._update_q()
            # self._update_pi()
            self.episode = []  # inicializo de nuevo los episodios

    def _update_q(self):
        G = 0
        self.episode.reverse()
        states_actions = []
        [
            states_actions.append((state, action))
            for state, action, _ in self.episode
            if (state, action) not in states_actions
        ]
        reward = self.episode[0][2]
        state_t= self.episode[0][0]
        action_t = self.episode[0][1]
        # for state, action in states_actions:
            # first_occurence = next(
            #     i
            #     for i, step in enumerate(self.episode)
            #     if step[0] == state and step[1] == action
            # )
        # print(self.episode)
        for state, action, reward_a in self.episode[1:]:
            G = self.gamma*G + reward
            reward = reward_a
            # print('G', G)
            
            if (state_t, action_t) in states_actions[0:len(states_actions)-2]:
                self.returns[state_t][action_t] = G
                self.returns_n[state_t][action_t] = np.average(
                    self.returns[state_t][action_t])
                self.q[state_t][action_t] = self.returns_n[state_t][action_t]
                # if(np.argmax(self.q[state][action])!=self.pi[0][0]):
                print('np.argmax',np.argmax(self.q[state_t]), action)
                self.pi[state_t] = np.argmax(self.q[state_t][action])

    # def _update_pi(self):
    #     states = []
    #     [states.append(state)
    #      for state, _, _ in self.episode if state in states]
    #     for state in states:
    #         best_action = np.argmax(self.actions_n,self.q[state])
    #         self.pi[state] = best_action

    def get_action(self, state):
        # print('q', self.q)
        # print('pi', self.pi, state)
        probability = 0
        isZero = False
        for action in self.pi[state]:
            if action > 0:
                probability+=action
            else:
                isZero = True
        if isZero != True and probability ==1:
            # print('p en 1',)
            return np.random.choice(self.actions_n, p=self.pi[state])
        else:
            # print("p no 1")
            return -1
            
        

    def get_best_action(self, state):
        return np.argmax(self.q[state])

    def render(self):
        print(f"Values: {self.q}\nPolicy: {self.pi}")
