from string import ascii_lowercase
import random
from itertools import combinations
import numpy as np

def create_problem(n, k, m):
    positive_var = list(ascii_lowercase)[:n]
    negative_var = [var.upper() for var in positive_var]
    variables = positive_var + negative_var
    problem = []
    threshold = 10
    i = 0
    comb = list(combinations(variables, k))

    while i < threshold:
        c = random.sample(comb, m)
        if c not in problem:
            problem.append(c)
            i += 1

    problems_new = []
    for c in problem:
        temp = []
        temp = [list(sub) for sub in c]
        problems_new.append(temp)
    return variables, problems_new


def random_assign(variables, n):
    litral = list(np.random.choice(2, n))
    negation = [abs(i - 1) for i in litral]
    assign = litral + negation
    return dict(zip(variables, assign))


def heuristic(problem, assign):
    count = 0
    for sub in problem:
        encode = [assign[val] for val in sub]
        count += any(encode)
    return count


def next_node(current):
    key = list(current.keys())
    key.sort()
    key = key[0:len(key) // 2]
    successors = []
    for k in key:
        temp = current.copy()
        temp[k] = abs(temp[k] - 1)
        temp[chr(ord(k) + 32)] = abs(temp[chr(ord(k) + 32)] - 1)
        successors.append(temp)

    return successors

    print(next_node({'a': 0, 'b': 0, 'c': 0, 'A': 1, 'B': 1, 'C': 1}))
    
def select_node(succs, problem):
    heuristic_val = []
    for i in succs:
        heuristic_val.append(heuristic(problem, i))
    index = heuristic_val.index(max(heuristic_val))
    return succs[index]


def check_goal_state(state, problem):
    count = 0
    for sub in problem:
        encode = [state[val] for val in sub]
        count += any(encode)
    return len(problem) == count

#Hill Climbing
print("\nHill Climbing: \n")
def hill_climbing(current_state, problem, step):
    if step == 10000:
        print('halted at depth', step)
        return
    if check_goal_state(current_state, problem) == True:
        print(current_state, step)
        return
    else:
        step += 1
        successor = next_node(current_state)
        new_node = select_node(successor, problem)
        hill_climbing(new_node, problem, step)


n = 2
k = 3
m = 2
var, prob = create_problem(n, k, m)
print(var)
for i in prob:
    print(i)

start_state = random_assign(var, n)
print(start_state, prob[0])
hill_climbing(start_state, prob[0], 0)
print(check_goal_state({'a': 0, 'b': 1, 'c': 0, 'd': 1, 'A': 1, 'B': 0, 'C': 1, 'D': 0},prob[7]))


# Beam search 
print("\nBeam search: \n")
def heuristic(problem, assign):
    count = 0
    for sub in problem:
        encode = [assign[val] for val in sub]
        count += any(encode)
    return count

def check_goal_state(state, problem):
    count = 0
    for sub in problem:
        encode = [state[val] for val in sub]
        count += any(encode)
    return len(problem) == count

def select_node_beam(succs, problem, beamwidth):
    heuristic_vals = []
    for i in succs:
        heuristic_vals.append(heuristic(problem, i))
    beam_nodes = []
    for i in range(beamwidth):
        index = heuristic_vals.index(max(heuristic_vals))
        beam_nodes.append(succs[index])
        heuristic_vals.remove(heuristic_vals[index])
    return beam_nodes

def next_node_beam(succs):
    next_nodes = []
    for current in succs:
        key = list(current.keys())
        key.sort()
        key = key[0:len(key) // 2]
        for k in key:
            temp = current.copy()
            temp[k] = abs(temp[k] - 1)
            temp[chr(ord(k) + 32)] = abs(temp[chr(ord(k) + 32)] - 1)
            next_nodes.append(temp)
    return next_nodes

def beam_search(start, problem, step, beamwidth):
    if step == 10000:
        print('halted at depth', step)
        return
    for current_state in start:
        if check_goal_state(current_state, problem):
            print(current_state, step)
            return
    step += 1
    successor = next_node_beam(start)
    new_nodes = select_node_beam(successor, problem, beamwidth)
    beam_search(new_nodes, problem, step, beamwidth)
    
    n = 5
    k = 3
    m = 5
    var,probl = create_problem(n,k,m)
    print(var)
    for i in probl:
        print(i)
    start_state = random_assign(var,n)
    print([start_state,start_state])
    
# Beam width should not exceed number of variable
beam_search([start_state, start_state], prob[2], 0, 1)
        

# Variable-Neighborhood-Descent with 3 neighborhood functions
print("\nVariable-Neighborhood-Descent 1: \n")
def nghd1(current):
    key = list(current.keys())
    key.sort()
    key = key[0:len(key) // 2]
    successors = []
    for k in key:
        temp = current.copy()
        temp[k] = abs(temp[k] - 1)
        temp[chr(ord(k) + 32)] = abs(temp[chr(ord(k) + 32)] - 1)
        successors.append(temp)
    return successors

print(nghd1({'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}))
print("\nVariable-Neighborhood-Descent 2: \n")
def nghd2(current):
    key = list(current.keys())
    key.sort()
    key = key[0:len(key) // 2]
    successors = []
    for j in range(0, len(key) - 1):
        for i in range(j, len(key) - 1):
            temp = current.copy()
            temp[key[i]] = abs(temp[key[i]] - 1)
            temp[key[i + 1]] = abs(temp[key[i + 1]] - 1)
            temp[chr(ord(key[i]) + 32)] = abs(temp[chr(ord(key[i]) + 32)] - 1)
            temp[chr(ord(key[i + 1]) + 32)] = abs(temp[chr(ord(key[i + 1]) + 32)] - 1)
            successors.append(temp)
    return successors

print(nghd2({'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}))
print("\nVariable-Neighborhood-Descent 3: \n")
def nghd3(current):
    key = list(current.keys())
    key.sort()
    key = key[0:len(key) // 2]
    successors = []
    for j in range(0, len(key) - 2):
        for k in range(j, len(key) - 2):
            for i in range(k, len(key) - 2):
                temp = current.copy()
                temp[key[i]] = abs(temp[key[i]] - 1)
                temp[key[i + 1]] = abs(temp[key[i + 1]] - 1)
                temp[chr(ord(key[i]) + 32)] = abs(temp[chr(ord(key[i]) + 32)] - 1)
                temp[chr(ord(key[i + 1]) + 32)] = abs(temp[chr(ord(key[i + 1]) + 32)] - 1)
                successors.append(temp)
    return successors

print(nghd3({'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}))

print("\n \n")
def Variable_Neighborhood(current_state, problem, step):
    if step == 10000:
        print('halted at depth', step)
        return
    if check_goal_state(current_state, problem):
        print(current_state, step)
        return current_state
    else:
        step += 1
        successor = next_node(current_state)
        new_node = nghd1(successor)
        Variable_Neighborhood(new_node, problem, step)
print("\n \n")
        
def Variable_Neighborhood2(current_state, problem, step):
    if step == 10000:
        print('halted at depth', step)
        return 
    if check_goal_state(current_state, problem):
        return current_state
    else:
        step += 1
        successor = next_node(current_state)
        new_node = nghd2(successor)
        return Variable_Neighborhood2(new_node, problem, step)
print("\n \n")
def Variable_Neighborhood3(current_state, problem, step):
    if step == 10000:
        print('halted at depth', step)
        return
    if check_goal_state(current_state, problem):
        print(current_state, step)
        return current_state
    else:
        step += 1
        successor = next_node(current_state)
        new_node = nghd3(successor)
        return Variable_Neighborhood3(new_node, problem, step)


n = 5
k = 3
m = 5
var, probl = create_problem(n, k, m)
print(var)
for i in probl:
    print(i)

start_state = random_assign(var, n)
print([start_state, start_state])

var1 = start_state
var2 = Variable_Neighborhood(var1,prob[0],0)
var3 = Variable_Neighborhood2(var2,prob[0],0)
Variable_Neighborhood(var3,prob[0],0)
