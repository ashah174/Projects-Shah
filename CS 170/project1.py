import heapq
import copy

class PuzzleNode:
    def __init__(self, state, parent=None, move=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.cost = cost  # g(n)
        self.heuristic = heuristic  # h(n)
        self.total_cost = self.cost + self.heuristic  # f(n) = g(n) + h(n)
    
    def __lt__(self, other):
        return self.total_cost < other.total_cost

def find_blank(state):
    for i, row in enumerate(state):
        for j, val in enumerate(row):
            if val == 0:
                return i, j

def generate_moves(state):
    x, y = find_blank(state)
    moves = []
    if x > 0: moves.append((x - 1, y))  # Move up
    if x < 2: moves.append((x + 1, y))  # Move down
    if y > 0: moves.append((x, y - 1))  # Move left
    if y < 2: moves.append((x, y + 1))  # Move right
    return moves

def make_move(state, move):
    x, y = find_blank(state)
    new_state = copy.deepcopy(state)
    new_x, new_y = move
    new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
    return new_state

def misplaced_tile_heuristic(state, goal):
    return sum(1 for i in range(3) for j in range(3) if state[i][j] != goal[i][j] and state[i][j] != 0)

def manhattan_distance_heuristic(state, goal):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                goal_x, goal_y = divmod(goal.index(state[i][j]), 3)
                distance += abs(i - goal_x) + abs(j - goal_y)
    return distance

def general_search(initial_state, goal_state, heuristic_func):
    frontier = []
    explored = set()
    heapq.heappush(frontier, PuzzleNode(initial_state, cost=0, heuristic=heuristic_func(initial_state, goal_state)))
    
    while frontier:
        node = heapq.heappop(frontier)
        explored.add(tuple(map(tuple, node.state)))
        
        if node.state == goal_state:
            return node
        
        for move in generate_moves(node.state):
            new_state = make_move(node.state, move)
            if tuple(map(tuple, new_state)) not in explored:
                heapq.heappush(frontier, PuzzleNode(new_state, node, move, node.cost + 1, heuristic_func(new_state, goal_state)))
    
    return None

def print_solution(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    for state in reversed(path):
        for row in state:
            print(row)
        print()

def main():
    initial_state = [[1, 2, 3], [4, 0, 5], [7, 8, 6]]
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    
    print("Solving using Uniform Cost Search:")
    solution = general_search(initial_state, goal_state, lambda s, g: 0)
    print_solution(solution)
    
    print("Solving using A* with Misplaced Tile Heuristic:")
    solution = general_search(initial_state, goal_state, misplaced_tile_heuristic)
    print_solution(solution)
    
    print("Solving using A* with Manhattan Distance Heuristic:")
    solution = general_search(initial_state, goal_state, manhattan_distance_heuristic)
    print_solution(solution)

if __name__ == "__main__":
    main()