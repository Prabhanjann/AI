from collections import deque

# Directions for movement
MOVES = {
    'Up': -3,
    'Down': 3,
    'Left': -1,
    'Right': 1
}

# Define the goal state
GOAL_STATE = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)

# Valid indices for moves
def valid_moves(index):
    moves = []
    row, col = divmod(index, 3)

    if row > 0: moves.append('Up')
    if row < 2: moves.append('Down')
    if col > 0: moves.append('Left')
    if col < 2: moves.append('Right')

    return moves

# Apply move to a state
def apply_move(state, move):
    idx = state.index(0)
    new_idx = idx + MOVES[move]

    # Special case for left/right edge wrapping
    if move == 'Left' and idx % 3 == 0:
        return None
    if move == 'Right' and idx % 3 == 2:
        return None

    state = list(state)
    state[idx], state[new_idx] = state[new_idx], state[idx]
    return tuple(state)

# DFS with depth limit
def dls(state, depth, visited, path):
    if state == GOAL_STATE:
        return path

    if depth == 0:
        return None

    visited.add(state)
    for move in valid_moves(state.index(0)):
        next_state = apply_move(state, move)
        if next_state and next_state not in visited:
            result = dls(next_state, depth - 1, visited.copy(), path + [(move, next_state)])
            if result:
                return result
    return None

# IDDFS main function
def iddfs(start_state, max_depth=50):
    for depth in range(max_depth):
        print(f"\n--- Iteration {depth + 1}: Depth Limit = {depth} ---")
        visited = set()
        path = dls(start_state, depth, visited, [])
        if path is not None:
            return path
    return None

# Function to print the puzzle state in a readable format
def print_state(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

# Example usage
if __name__ == '__main__':
    start = (1, 2, 3,
            4, 0, 5,
            7, 8, 6)

    print("Initial State:")
    print_state(start)

    solution = iddfs(start)
    if solution:
        print(f"Solution found in {len(solution)} moves:")
        current_state = start
        for move, state in solution:
            print(f"Move: {move}")
            print_state(state)
            current_state = state
    else:
        print("No solution found.")
