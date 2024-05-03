import random
import math
import matplotlib.pyplot as plt

def calculate_total_distance(tour, distances):
    # Calculate the total distance of a tour based on the distances between cities.
    total_dist = 0
    for i in range(len(tour)):
        total_dist += distances[tour[i - 1]][tour[i]]
    return total_dist

def generate_random_tour(num_cities):
    # Generate a random tour of cities.
    tour = list(range(num_cities))
    random.shuffle(tour)
    return tour

def perturb_tour(tour):
    # Perturb a tour by randomly swapping two cities.
    i, j = sorted(random.sample(range(len(tour)), 2))
    tour[i:j + 1] = reversed(tour[i:j + 1])
    return tour

def simulated_annealing(distances, max_iter, init_temp, cool_rate):
    # Use simulated annealing to find the shortest path to visit all cities.
    num_cities = len(distances)
    current_tour = generate_random_tour(num_cities)
    current_dist = calculate_total_distance(current_tour, distances)
    best_tour = current_tour[:]
    best_dist = current_dist
    temperature = init_temp

    for iteration in range(max_iter):
        new_tour = perturb_tour(current_tour)
        new_dist = calculate_total_distance(new_tour, distances)

        # Accept the new tour if it's shorter or with a certain probability
        if new_dist < current_dist or random.random() < math.exp((current_dist - new_dist) / temperature):
            current_tour = new_tour
            current_dist = new_dist

        # Update the best tour if needed
        if current_dist < best_dist:
            best_tour = current_tour[:]
            best_dist = current_dist

        temperature *= cool_rate

    return best_tour, best_dist

# Define the distances between cities
city_distances = [
    [0, 12, 3, 23, 1],
    [12, 0, 9, 18, 3],
    [3, 9, 0, 89, 56],
    [23, 18, 89, 0, 45],
    [1, 3, 56, 45, 0]
]

# Set the parameters for the simulated annealing algorithm
max_iterations = 100
initial_temperature = 1000
cooling_rate = 0.99

# Perform the simulated annealing
best_path, best_distance = simulated_annealing(city_distances, max_iterations, initial_temperature, cooling_rate)

# Plot the best path
num_cities = len(city_distances)
x_coords = [random.random() * 100 for _ in range(num_cities)]
y_coords = [random.random() * 100 for _ in range(num_cities)]
plt.figure(figsize=(8, 6))
plt.scatter(x_coords, y_coords, c='blue', s=100)
for i, txt in enumerate(range(num_cities)):
    plt.annotate(txt, (x_coords[i], y_coords[i]), fontsize=12)
for i in range(num_cities - 1):
    plt.plot([x_coords[best_path[i]], x_coords[best_path[i + 1]]], [y_coords[best_path[i]], y_coords[best_path[i + 1]]], c='red')
plt.plot([x_coords[best_path[-1]], x_coords[best_path[0]]], [y_coords[best_path[-1]], y_coords[best_path[0]]], c='red')
plt.title("Traveling Salesman Problem - Best Tour")
plt.xlabel("X-coordinate")
plt.ylabel("Y-coordinate")
plt.grid(True)
plt.show()

# Print the best path, its distance, and the final temperature after cooling
print("Best Path:", best_path)
print("Best Distance:", best_distance)
print("Final Temperature:", initial_temperature * (cooling_rate ** max_iterations))
