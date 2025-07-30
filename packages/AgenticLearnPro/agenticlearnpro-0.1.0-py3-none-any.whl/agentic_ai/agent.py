import numpy as np

class QLearningAgent:
    def __init__(self, state_space, action_space, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0):
        self.q_table = np.zeros((state_space, action_space))
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.action_space = action_space

    def choose_action(self, state):
        if np.random.uniform(0, 1) < self.exploration_rate:
            return np.random.choice(self.action_space)  # Explore
        return np.argmax(self.q_table[state])  # Exploit

    def learn(self, state, action, reward, next_state):
        current_q = self.q_table[state, action]
        next_max_q = np.max(self.q_table[next_state])
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_max_q - current_q)
        self.q_table[state, action] = new_q

    def decay_exploration(self, decay_rate=0.995, min_rate=0.1):
        self.exploration_rate = max(min_rate, self.exploration_rate * decay_rate)

def main():
    from environment import SimpleEnv

    env = SimpleEnv()
    agent = QLearningAgent(state_space=env.state_space, action_space=env.action_space)

    for episode in range(100):
        state = env.reset()
        done = False
        while not done:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            agent.learn(state, action, reward, next_state)
            state = next_state
        agent.decay_exploration()
    print("Q-table after training:", agent.q_table)

if __name__ == "__main__":
    main()