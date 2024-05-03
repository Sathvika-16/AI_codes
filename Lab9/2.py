import random

class NonstationaryBandit:
    def __init__(self, num_arms):
        self.num_arms = num_arms
        self.exp_rewards = [10] * num_arms
    
    def actions(self):
        return list(range(self.num_arms))
    
    def reward(self, action):
        # Update mean rewards with random walks
        for i in range(len(self.exp_rewards)):
            self.exp_rewards[i] += random.gauss(0, 0.1)
        # Generate reward with Gaussian noise
        return self.exp_rewards[action] + random.gauss(0, 0.01)

def epsilon_greedy_nonstationary_bandit(my_bandit, epsilon, max_iterations):
    # Initialization
    Q = [0] * my_bandit.num_arms
    count = [0] * my_bandit.num_arms
    R = []
    R_avg = [0] * 1
    max_iter = max_iterations
    # Epsilon-Greedy Implementation
    for iteration in range(1, max_iter):
        if random.random() > epsilon:
            # Exploit - Choose action with maximum Q value
            action = Q.index(max(Q))
        else:
            # Explore - Choose a random action
            action = random.choice(my_bandit.actions())
        # Get reward for the chosen action
        reward = my_bandit.reward(action)
        R.append(reward)
        # Update action counts and Q values
        count[action] += 1
        Q[action] += (reward - Q[action]) / count[action]
        # Update average rewards
        R_avg.append(R_avg[iteration - 1] + (reward - R_avg[iteration - 1]) / iteration)
    return Q, R_avg, R

# Set seed for reproducibility
random.seed(10)

# Initialize nonstationary bandit with 10 arms
my_bandit = NonstationaryBandit(10)

# Run epsilon-greedy algorithm
epsilon = 0.3
max_iterations = 10000
Q, R_avg, R = epsilon_greedy_nonstationary_bandit(my_bandit, epsilon, max_iterations)

# Display actual and recovered mean rewards
print("Actual\tRecovered ")
for actual, recovered in zip(my_bandit.exp_rewards, Q):
    print(f"{actual:.3f} \t {recovered:.3f}")

# Plot results
import matplotlib.pyplot as plt

# Plot average rewards vs iteration
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
ax1.plot(R_avg, color='LightSalmon')
ax1.set_title("Average Rewards vs Iteration")
ax1.set_xlabel("Iteration")
ax1.set_ylabel("Average Reward")

# Plot reward per iteration
ax2.plot(R, color='Cyan')
ax2.set_title("Reward per Iteration")
ax2.set_xlabel("Iteration")
ax2.set_ylabel("Reward")

plt.show()
