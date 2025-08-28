import heapq

goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]  

moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_valid(x, y):
    return 0 <= x < 3 and 0 <= y < 3

def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value == 0:
                continue
            goal_x, goal_y = divmod(value - 1, 3)
            distance += abs(i - goal_x) + abs(j - goal_y)
    return distance

def a_star(start_state):
    visited = set()
    priority_queue = []
    # f(n) = g(n) + h(n)
    heapq.heappush(priority_queue, (manhattan_distance(start_state), 0, start_state, [])) 

    while priority_queue:
        f, g, current_state, path = heapq.heappop(priority_queue)
        
        if current_state == goal_state:
            return path + [current_state]
        
        visited.add(state_to_tuple(current_state))
        x, y = find_blank(current_state)

        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                new_state = [row[:] for row in current_state]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                
                if state_to_tuple(new_state) not in visited:
                    g_new = g + 1
                    h_new = manhattan_distance(new_state)
                    f_new = g_new + h_new
                    heapq.heappush(priority_queue, (f_new, g_new, new_state, path + [current_state]))

    return None

start_state = [[1, 2, 3],
               [0, 4, 6],
               [7, 5, 8]]

solution_path = a_star(start_state)

if solution_path:
    print("Solution found in", len(solution_path) - 1, "moves:")
    for step in solution_path:
        for row in step:
            print(row)
        print("-----")
else:
    print("No solution found.")
