import time
import psutil

class Puzzle8:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

    def get_empty_tile_position(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return i, j

    def generate_successors(self, state):
        successors = []
        empty_i, empty_j = self.get_empty_tile_position(state)

        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

        for move in moves:
            new_i, new_j = empty_i + move[0], empty_j + move[1]

            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [row.copy() for row in state]
                new_state[empty_i][empty_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[empty_i][empty_j]
                successors.append(new_state)

        return successors

    def goal_test(self, state):
        return state == self.goal_state

    def iterative_deepening_search(self):
        depth = 0
        matrix_output = []

        cumulative_space_used = 0

        while True:
            start_time = time.time()
            start_memory = psutil.virtual_memory().used / (1024 ** 2)  # Memory in megabytes

            result, _ = self.depth_limited_search(self.initial_state, depth)

            end_time = time.time()
            end_memory = psutil.virtual_memory().used / (1024 ** 2)  # Memory in megabytes

            time_taken = end_time - start_time
            space_used = max(0, end_memory - start_memory)  # Ensure non-negative space used

            cumulative_space_used += space_used

            matrix_output.append([depth, time_taken, cumulative_space_used])

            if result == "goal":
                return matrix_output
            elif result == "cutoff":
                depth += 1
            else:
                return matrix_output

    def depth_limited_search(self, state, depth_limit):
        if self.goal_test(state):
            return "goal", 0

        if depth_limit == 0:
            return "cutoff", 0

        nodes_expanded = 0

        for successor in self.generate_successors(state):
            result, expanded = self.depth_limited_search(successor, depth_limit - 1)
            nodes_expanded += expanded

            if result == "goal":
                return "goal", nodes_expanded
            elif result == "cutoff":
                pass  

        return "cutoff", nodes_expanded

# Example Usage:
initial_state = [
    [4, 2, 3], [5, 1, 6],[7, 0, 8]
    ]
goal_state = [
    [1, 2, 3], [4, 5, 6],[7, 8, 0]
    ]

puzzle = Puzzle8(initial_state, goal_state)
result_matrix = puzzle.iterative_deepening_search()

# Display matrix-like output
print("\nDepth\tTime Taken\tCumulative Space Used")
for row in result_matrix:
    print("\t".join(map(str, row)))
