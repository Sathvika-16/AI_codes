from string import ascii_lowercase
import random
from itertools import combinations
import numpy as np

def create_problem(n, k, m):
    # Generate variables (lowercase and uppercase)
    positive_var = list(ascii_lowercase)[:n]
    negative_var = [var.upper() for var in positive_var]
    variables = positive_var + negative_var
    
    # Generate m random clauses of size k
    problem = []
    threshold = 10       
    i = 0
    comb = list(combinations(variables, k))
    
    while i < threshold:
        c = random.sample(comb, m)
        if c not in problem:
            problem.append(c)
            i += 1
    
    # Convert clauses to list of lists
    problems_new = []
    for c in problem:
        temp = [list(sub) for sub in c]
        problems_new.append(temp)
    
    return variables, problems_new 

def random_assign(variables, n):
    # Randomly assign truth values to variables
    litral = list(np.random.choice(2, n))
    negation = [abs(i - 1) for i in litral]
    assign = litral + negation
    return dict(zip(variables, assign))

# Define problem parameters
n = 5
k = 3
m = 3

# Create a 3-SAT problem instance
var, prob = create_problem(n, k, m)

# Print variables and clauses
print("Variables and clauses:")
print(var)
for i in prob:
    print(i)

# Print a random assignment
print("\nRandom assignment:")
print(random_assign(var, n))
