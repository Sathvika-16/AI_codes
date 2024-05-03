import random

class BinaryBandit:
    def __init__(self):
        # Number of arms
        self.num_arms = 2
        
    def get_actions(self):
        # Returns available actions
        return list(range(self.num_arms))
    
    def get_reward_probabilities(self):
        # Returns reward probabilities for each action
        return [0.1, 0.2]  # Example probabilities for reward 1
    
    def get_reward(self, action):
        # Returns reward for the given action based on its probability
        probabilities = self.get_reward_probabilities()
        rand = random.random()
        if rand < probabilities[action]:
            return 1
        else:
            return 0

def epsilon_greedy_bandit(binary_bandit, epsilon, max_iterations):
    # Initialization
    q_values = [0] * binary_bandit.num_arms
    action_counts = [0] * binary_bandit.num_arms
    rewards = []
    average_rewards = [0] * 1
    max_iter = max_iterations
    
    # Epsilon-Greedy Implementation
    for iteration in range(1, max_iter):
        if random.random() > epsilon:
            # Exploit - Choose action with maximum Q value
            action = q_values.index(max(q_values))
        else:
            # Explore - Choose a random action
            action = random.choice(binary_bandit.get_actions())
        
        # Get reward for the chosen action
        reward = binary_bandit.get_reward(action)
        rewards.append(reward)
        
        # Update action counts and Q values
        action_counts[action] += 1
        q_values[action] += (reward - q_values[action]) / action_counts[action]
        
        # Update average rewards
        average_rewards.append(average_rewards[iteration - 1] + (reward - average_rewards[iteration - 1]) / iteration)
    
    return q_values, average_rewards, rewards

# Initialize bandits
binary_bandit_A = BinaryBandit()
binary_bandit_B = BinaryBandit()

# Set seed for reproducibility
random.seed(10)

# Run epsilon-greedy algorithm for bandit A
epsilon = 0.2
max_iterations = 2000
Q_A, avg_rewards_A, rewards_A = epsilon_greedy_bandit(binary_bandit_A, epsilon, max_iterations)

# Run epsilon-greedy algorithm for bandit B
epsilon = 0.2  # Same epsilon value for consistency
Q_B, avg_rewards_B, rewards_B = epsilon_greedy_bandit(binary_bandit_B, epsilon, max_iterations)

# Display the results
import matplotlib.pyplot as plt

# Plot average rewards vs iteration for bandit A
plt.plot(avg_rewards_A, color = '#FF5733')
plt.title("Average Rewards vs Iteration (Bandit A)")
plt.xlabel("Iteration")
plt.ylabel("Average Reward")
plt.show()

# Plot average rewards vs iteration for bandit B
plt.plot(avg_rewards_B, color = 'Black')
plt.title("Average Rewards vs Iteration (Bandit B)")
plt.xlabel("Iteration")
plt.ylabel("Average Reward")
plt.show()


# Plot reward per iteration for bandit A
plt.plot(rewards_A, color = 'LightSalmon')
plt.title("Reward per Iteration (Bandit A)")
plt.xlabel("Iteration")
plt.ylabel("Reward")
plt.show()

# Plot reward per iteration for bandit B
plt.plot(rewards_B, color = 'Cyan')
plt.title("Reward per Iteration (Bandit B)")
plt.xlabel("Iteration")
plt.ylabel("Reward")
plt.show()
