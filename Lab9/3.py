import random

class Bandit(object):
    def __init__(self, N):
        self.N = N
        self.exp_rewards = [10] * N
    
    def actions(self):
        return list(range(self.N))
    
    def reward(self, action):
        # Update mean rewards with random walks
        for i in range(len(self.exp_rewards)):
            self.exp_rewards[i] += random.gauss(0, 0.1)
        # Generate reward with Gaussian noise
        return self.exp_rewards[action] + random.gauss(0, 0.01)

def eGreedy_modified(myBandit, epsilon, max_iteration, alpha):
    # Initialization
    Q = [0] * myBandit.N
    count = [0] * myBandit.N
    R = []
    R_avg = [0] * 1
    max_iter = max_iteration
    # Incremental Implementation
    for iter in range(1, max_iter):
        if random.random() > epsilon:
            # Exploit - Choose action with maximum Q value
            action = Q.index(max(Q))
        else:
            # Explore - Choose a random action
            action = random.choice(myBandit.actions())
        # Get reward for the chosen action
        reward = myBandit.reward(action)
        R.append(reward)
        # Update action counts and Q values with learning rate alpha
        count[action] += 1
        Q[action] += alpha * (reward - Q[action])
        # Update average rewards
        R_avg.append(R_avg[iter - 1] + (reward - R_avg[iter - 1]) / iter)
    return Q, R_avg, R

# Set seed for reproducibility
random.seed(10)

# Initialize bandit with 10 arms
myBandit = Bandit(N=10)

# Run modified epsilon-greedy algorithm
epsilon = 0.4
max_iterations = 10000
alpha = 0.01
Q, R_avg, R = eGreedy_modified(myBandit, epsilon, max_iterations, alpha)

# Display actual and recovered mean rewards
print("Actual\tRecovered ")
for actual, recovered in zip(myBandit.exp_rewards, Q):
    print(f"{actual:.3f} \t {recovered:.3f}")

# Plot results
import matplotlib.pyplot as plt

# Plot average rewards vs iteration
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
ax1.plot(R_avg, color='black')
ax1.set_title("Average Rewards vs Iteration")
ax1.set_xlabel("Iteration")
ax1.set_ylabel("Average Reward")

# Plot reward per iteration
ax2.plot(R, color='LightSalmon')
ax2.set_title("Reward per Iteration")
ax2.set_xlabel("Iteration")
ax2.set_ylabel("Reward")

plt.suptitle("Modified Epsilon Greedy Policy")
plt.show()
