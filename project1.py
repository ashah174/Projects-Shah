import heapq
import copy

# Node class to keep track of the puzzle state, parent, and costs
class Node:
    def __init__(self, state, parent, g, h):
        self.state = state  # Current puzzle state
        self.parent = parent  # Parent node
        self.g = g  # Cost from start to current state
        self.h = h  # Heuristic cost to goal
        self.f = g + h  # Total cost

    # For comparing nodes in the priority queue
    def __lt__(self, other):
        return self.f < other.f

# Function to get the puzzle from the user
def get_puzzle():
    print("Welcome to my 8-puzzle solver!")
    print("Choose an option:")
    print("1. Use the default puzzle")
    print("2. Enter your own puzzle")
    choice = input("Enter 1 or 2: ")

    if choice == "1":
        # Default puzzle (is already solved)
        return [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    elif choice == "2":
        print("Enter each row as three numbers separated by spaces (ex:'1 2 3').")
        row_one = input("Enter the first row: ")
        row_two = input("Enter the second row: ")
        row_three = input("Enter the third row: ")
        
        #Splits the input into individual numbers
        row_one = row_one.split()
        row_two = row_two.split()
        row_three = row_three.split()

        # This is to validate the input to make sure it is a 3x3 puzzle
        if len(row_one) != 3 or len(row_two) != 3 or len(row_three) != 3:
            print("Each row must contain exactly 3 numbers. Exiting.")
            exit()

        # Converts the input into intgers and creats the puzzle 
        user_puzzle = [[int(num) for num in row_one],
                       [int(num) for num in row_two],
                       [int(num) for num in row_three]]
        return user_puzzle
    else:
        print("Invalid choice. Exiting.")
        exit()

# Heuristic 1: This algortith counts the number of misplaced tiles excluding the blank tile
def misplaced_tiles(state, goal): 
    count = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != goal[i][j] and state[i][j] != 0:
                count += 1
    return count

# Heuristic 2: This algorthim calculates the manhattan distance of each tile from its goal position
def manhattan_distance(state, goal):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                # Calculates the correct postion of the tile and adds the distance to the total
                correct_row = (state[i][j] - 1) // 3
                correct_col = (state[i][j] - 1) % 3
                distance += abs(i - correct_row) + abs(j - correct_col)
    return distance

# Finds the position of the blank tile or 0 in the puzzle
def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return None

# Generate all possible moves from the current state
def get_moves(state):
    moves = []
    blank_position = find_blank(state)
    if blank_position is None:
        return moves
    empty_row, empty_col = blank_position

    # Moving Up: Swaps the blank tile with the tile above it
    if empty_row > 0:
        new_up = copy.deepcopy(state)
        new_row_up = empty_row - 1
        new_up[empty_row][empty_col], new_up[new_row_up][empty_col] = new_up[new_row_up][empty_col], new_up[empty_row][empty_col]
        moves.append(new_up)

    # Moving Down: Swaps the blank tile with the tile below it
    if empty_row < 2:
        new_down = copy.deepcopy(state)
        new_row_down = empty_row + 1
        new_down[empty_row][empty_col], new_down[new_row_down][empty_col] = new_down[new_row_down][empty_col], new_down[empty_row][empty_col]
        moves.append(new_down)

    # Moving Left: Swaps the blank tile with the tile to the left of it
    if empty_col > 0:
        new_left = copy.deepcopy(state)
        new_col_left = empty_col - 1
        new_left[empty_row][empty_col], new_left[empty_row][new_col_left] = new_left[empty_row][new_col_left], new_left[empty_row][empty_col]
        moves.append(new_left)

    # Moving Right: Swaps the blank tile with the tile to the right of it
    if empty_col < 2:
        new_right = copy.deepcopy(state)
        new_col_right = empty_col + 1
        new_right[empty_row][empty_col], new_right[empty_row][new_col_right] = new_right[empty_row][new_col_right], new_right[empty_row][empty_col]
        moves.append(new_right)

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

    nodes_expanded = 0  #Counter for the number of nodes that have been expanded
    max_queue_size = 1  #Tracks the maxium size of the queue during the search
    #pop the node with the lowest cost from the priority queue
    while open_list:
        current_node = heapq.heappop(open_list)

        # Checks to see if we have reached the goal state
        if current_node.state == goal_state:
            return current_node, nodes_expanded, max_queue_size

        # Adds the current state to the closed set so that it avoids being expanded again
        closed_set.add(tuple(map(tuple, current_node.state)))

        # This generates all the possible moves from the current state and adds them to the open list
        for move in get_moves(current_node.state):
            if tuple(map(tuple, move)) not in closed_set:
                g = current_node.g + 1  # Increment the cost which is the number of  moves
                h = heuristic(move, goal_state)  # Calculate heuristic
                f = g + h  # Total cost
                #Creates a new mode and then adds it to the priority queue
                new_node = Node(move, current_node, g, h)
                heapq.heappush(open_list, new_node)
                nodes_expanded += 1 

        # Update the maximum queue size
        max_queue_size = max(max_queue_size, len(open_list))

    # reurn None if no solution is found
    return None, nodes_expanded, max_queue_size

# Print the solution path from the start state to the goal state
def print_solution(node):
    if node is None:
        print("No solution found.")
        return
    #traces the path from the goal state to the start state
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
    #This gets the initial puzzle state from the user
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
        exit()

    #Print the soluton and the statistics
    print_solution(solution)
    if solution:
        print("Solution found!")
        print(f"Solution depth: {solution.g}")
        print(f"Nodes expanded: {nodes_expanded}")
        print(f"Max queue size: {max_queue_size}")
    else:
        print("No solution found.")


if __name__ == "__main__":
    main()