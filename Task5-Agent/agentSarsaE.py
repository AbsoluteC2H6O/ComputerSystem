import numpy as np


class EXPECTEDSARSA:
    def __init__(self, states_n, actions_n, alpha, gamma, epsilon):
        self.states_n = states_n
        self.actions_n = actions_n
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.reset()

    def reset(self):
        self.episode = 0
        self.step = 0
        self.state = 0
        self.action = 0
        self.next_state = 0
        self.next_action = 0
        self.reward = 0
        self.done = False
        self.q_table = np.zeros((self.states_n, self.actions_n))

    def update(
        self, state, action, next_state, next_action, reward, terminated, truncated
    ):
        self._update(
            state, action, next_state, next_action, reward, terminated, truncated
        )
        best_action = np.argmax(self.q_table[self.next_state, :])
        non_greedy = self.epsilon / self.actions_n

        greedy_actions = [1-self.epsilon + non_greedy if qvlues ==
                          best_action else non_greedy for qvlues in range(len(self.q_table[self.next_state, :]))]

        expectedSarsavalues = [
            greedy_actions[qvlues]*self.q_table[next_state, qvlues] for qvlues in range(len(self.q_table[self.next_state, :]))
        ]

        self.q_table[state, action] = self.q_table[state, action] + self.alpha*(
            reward + self.gamma *
            np.sum(expectedSarsavalues)-self.q_table[state, action]
        )

    def _update(
        self, state, action, next_state, next_action, reward, terminated, truncated
    ):
        if self.done:
            self.step = 0
            self.done = False

        self.step += 1
        self.state = state
        self.action = action
        self.next_state = next_state
        self.next_action = next_action
        self.reward = reward

        if terminated or truncated:
            self.episode += 1
            self.done = True

    def get_action(self, state, mode):
        if mode == "random":
            return np.random.choice(self.actions_n)
        elif mode == "greedy":
            return np.argmax(self.q_table[state])
        elif mode == "epsilon-greedy":
            if np.random.uniform(0, 1) < self.epsilon:
                return np.random.choice(self.actions_n)
            else:
                return np.argmax(self.q_table[state])

    def render(self, mode="step"):
        if mode == "step":
            print(
                f"Episode: {self.episode}, Step: {self.step}, State: {self.state}, Action: {self.action}, ",
                end="",
            )
            print(
                f"Next state: {self.next_state}, Next action: {self.next_action}, Reward: {self.reward}"
            )

        elif mode == "values":
            print(f"Q-Table: {self.q_table}")
