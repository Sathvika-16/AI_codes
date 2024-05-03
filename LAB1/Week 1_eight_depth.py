import itertools

def generate_all_instances(goal_state, depth):
    all_instances = set()
    generate_instances_recursively(goal_state, depth, [], all_instances)
    return all_instances

def generate_instances_recursively(state, depth, path, all_instances):
    if depth == 0:
        all_instances.add(tuple(map(tuple, state)))
        return
    legal_moves = get_legal_moves(state)
    for move in legal_moves:
        next_state = [row.copy() for row in state]
        apply_move(next_state, move)
        generate_instances_recursively(next_state, depth - 1, path + [move], all_instances)

def get_legal_moves(puzzle):
    empty_index = [(i, row.index(0)) for i, row in enumerate(puzzle) if 0 in row][0]
    legal_moves = []
    if empty_index[1] > 0:
        legal_moves.append('left')
    if empty_index[1] < 2:
        legal_moves.append('right')
    if empty_index[0] > 0:
        legal_moves.append('up')
    if empty_index[0] < 2:
        legal_moves.append('down')
    return legal_moves

def apply_move(puzzle, move):
    empty_index = [(i, row.index(0)) for i, row in enumerate(puzzle) if 0 in row][0]
    row, col = empty_index
    if move == 'left':
        puzzle[row][col], puzzle[row][col - 1] = puzzle[row][col - 1], puzzle[row][col]
    elif move == 'right':
        puzzle[row][col], puzzle[row][col + 1] = puzzle[row][col + 1], puzzle[row][col]
    elif move == 'up':
        puzzle[row][col], puzzle[row - 1][col] = puzzle[row - 1][col], puzzle[row][col]
    elif move == 'down':
        puzzle[row][col], puzzle[row + 1][col] = puzzle[row + 1][col], puzzle[row][col]

def print_all_instances(initial_state, all_instances):
    print("Initial Input:")
    for row in initial_state:
        print(row)
    print()

    for i, instance in enumerate(all_instances, 1):
        print(f"Instance {i}:")
        for row in instance:
            print(row)
        print()

# Example usage:
goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]  
depth = 2

initial_state = [[4, 2, 3],[5, 1, 6],[7, 0, 8]]

all_instances = generate_all_instances(initial_state, depth)
print_all_instances(initial_state, all_instances)
