def dls(node, target, depth, tree, visited):
    if depth < 0:
        return False

    visited.append(node)

    if node == target:
        return True

    if node not in tree:
        return False

    for child in tree[node]:
        if dls(child, target, depth - 1, tree, visited):
            return True

    return False

def iddfs(root, target, max_depth, tree):
    visited = []

    # Iterate through each depth level
    for depth in range(max_depth + 1):
        # Clear the visited path before starting a new depth search
        visited_at_depth = []
        if dls(root, target, depth, tree, visited_at_depth):
            print(f"Depth {depth}: Traversal path to '{target}':", ' → '.join(visited_at_depth))
            break
        else:
            print(f"Depth {depth}: No path found to '{target}'. Traversal path:", ' → '.join(visited_at_depth))
    
    return visited_at_depth

# Define the tree
tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['H'],
    'E': ['I'],
}

# Run IDDFS
trace = iddfs('A', 'G', 4, tree)
