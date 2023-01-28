import numpy as np

class ValueIteration():
    def __init__(self, states_n, actions_n, P, gamma):
        self.states_n = states_n
        self.actions_n = actions_n
        self.P = P
        self.gamma = gamma
        self.reset()

    def reset(self):
        self.values = np.zeros(self.states_n)
        self.policy = np.zeros(self.states_n)

    def get_action(self, state):
        return int(self.policy[state])

    def render(self):
        print("Values: ", self.values, "\nPolicy: ", self.policy)

    def solve(self, iterations, modo):
        if(modo == 'value'):
            print("Mood Value")
            for _ in range(iterations):
                for s in range(self.states_n):
                    values = [sum([prob * (r + self.gamma * self.values[s_])
                                for prob, s_, r, _ in self.P[s][a]])
                            for a in range(self.actions_n)]
                    self.values[s] = max(values)
                    self.policy[s] = np.argmax(np.array(values))

        elif(modo == 'policy'):
            print("Mood Policy")
            # Initialitazion
            self.values = np.zeros(self.states_n)
            self.policy = np.zeros(self.states_n)
            diff = 0
            theta = 1e-8 # error
            while True:
                while True:
                # Policy Evaluation
                    for s in range(self.states_n):
                        valueActual = [sum([prob * (r + self.gamma * self.values[s_])
                                    for prob, s_, r, _ in self.P[s][self.policy[s]]])]
                        self.values[s] = np.array(valueActual)
                        diff = max(diff, abs(valueActual - self.values[s]))
                    if diff < theta:
                        break
                # Policy Improvement
                policy_stable = True
                for s in range(self.states_n):
                    best = self.policy[s]
                    self.policy[s] = np.argmax([sum([prob * (r + self.gamma * self.values[s_])
                            for prob, s_, r, _ in self.P[s][a]])
                            for a in range(self.actions_n)])
                    if(best != self.policy[s]):
                        policy_stable = False
                if policy_stable:
                    break