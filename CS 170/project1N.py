import heapq
import copy

class Node:
    def __init__(self, state, parent, g, h):
        self.state = state
        self.parent = parent
        self.g = g  # Cost from start to current state
        self.h = h  # Heuristic cost to goal
        self.f = g + h  # Total cost

    def __lt__(self, other):
        return self.f < other.f

# Function to get user input for the puzzle
def get_puzzle():
    print("Hello! Welcome to my 8-puzzle game")
    print("Choose an output:")
    print("1. Use the default puzzle")
    print("2. Enter your own puzzle")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        return [[1, 2, 3], [4, 0, 5], [7, 8, 6]]
    elif choice == '2':
        puzzle = []
        print("Enter the puzzle row by row, using 0 for the blank space.")
        for i in range(3):
            row = list(map(int, input(f"Enter row {i + 1}: ").split()))
            puzzle.append(row)
        return puzzle
    else:
        print("Invalid choice. Please try again.")
        return get_puzzle()

# Heuristic 1: Count misplaced tiles
def misplaced_tiles(state, goal):
    count = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != goal[i][j]:
                count += 1
    return count

# Heuristic 2: Calculate Manhattan distance
def manhattan_distance(state, goal):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                # Find the correct position for the current tile
                correct_row = (state[i][j] - 1) // 3
                correct_col = (state[i][j] - 1) % 3
                distance += abs(i - correct_row) + abs(j - correct_col)
    return distance

# Find the position of the blank tile (0)
def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return None

# Generate all possible moves from the current state
def get_moves(state):
    moves = []
    blank_row, blank_col = find_blank(state)

    # Possible directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in directions:
        new_row, new_col = blank_row + dr, blank_col + dc

        # Check if the new position is within bounds
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = copy.deepcopy(state)
            # Swap the blank tile with the adjacent tile
            new_state[blank_row][blank_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[blank_row][blank_col]
            moves.append(new_state)

    return moves

# Uniform Cost Search (A* with heuristic = 0)
def uniform_cost(initial_state, goal_state):
    return a_star(initial_state, goal_state, heuristic=lambda x, y: 0)

# A* Search Algorithm
def a_star(initial_state, goal_state, heuristic):
    open_list = []  # Priority queue for nodes to explore
    closed_set = set()  # Set of explored states

    # Start with the initial state
    start_node = Node(initial_state, None, 0, heuristic(initial_state, goal_state))
    heapq.heappush(open_list, start_node)

    nodes_expanded = 0
    max_queue_size = 1

    while open_list:
        current_node = heapq.heappop(open_list)

        # Check if we've reached the goal
        if current_node.state == goal_state:
            return current_node, nodes_expanded, max_queue_size

        # Add the current state to the closed set
        closed_set.add(tuple(map(tuple, current_node.state)))

        # Generate all possible moves
        for move in get_moves(current_node.state):
            if tuple(map(tuple, move)) not in closed_set:
                g = current_node.g + 1  # Increment the cost
                h = heuristic(move, goal_state)  # Calculate heuristic
                f = g + h  # Total cost

                new_node = Node(move, current_node, g, h)
                heapq.heappush(open_list, new_node)
                nodes_expanded += 1

        # Update the maximum queue size
        max_queue_size = max(max_queue_size, len(open_list))

    # If no solution is found
    return None, nodes_expanded, max_queue_size

# Print the solution path
def print_solution(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent

    # Print the path from start to goal
    for state in reversed(path):
        for row in state:
            print(row)
        print()

# Main function
def main():
    initial_state = get_puzzle()
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    print("Choose an algorithm:")
    print("1. Uniform Cost Search")
    print("2. A* with Misplaced Tile Heuristic")
    print("3. A* with Manhattan Distance Heuristic")
    choice = input("Enter 1, 2, or 3: ")

    if choice == "1":
        solution, nodes_expanded, max_queue_size = uniform_cost(initial_state, goal_state)
    elif choice == "2":
        solution, nodes_expanded, max_queue_size = a_star(initial_state, goal_state, misplaced_tiles)
    elif choice == "3":
        solution, nodes_expanded, max_queue_size = a_star(initial_state, goal_state, manhattan_distance)
    else:
        print("Invalid choice. Exiting.")
        return

    if solution:
        print("Solution found:")
        print_solution(solution)
        print(f"Solution depth: {solution.g}")
        print(f"Nodes expanded: {nodes_expanded}")
        print(f"Max queue size: {max_queue_size}")
    else:
        print("No solution found.")

# Run the program
if __name__ == "__main__":
    main()