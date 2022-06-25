
def solve_internal(input_state, goal_function, distance_function, heuristic_function, neighbor_function, depth=None):
    if isinstance(input_state, list):
        input_state = tuple(input_state)

    open_set = []  # Discovered nodes that may need to be (re-)expanded.
    came_from = {}  # To reconstruct the path
    g_score = {}  # Map of node to cheapest path to start from that node
    f_score = {}  # g_score + h
    iterations = 0

    open_set.append(input_state)  # Add start node to open set
    g_score[input_state] = 0  # Start node has no cost
    f_score[input_state] = heuristic_function(input_state) # Init start node's f_score
    
    def reconstruct_path(current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        return total_path

    def get_next_node():
        current = None
        best_f = float('inf')
        for node in open_set:
            if f_score[node] < best_f:
                current = node
                best_f = f_score[node]
        return current

    while len(open_set) > 0:
        # Find node with lowest f_score
        current = get_next_node()
        #print("------> ", current)
        if iterations == depth and depth is not None:
            print("Reached depth limit")
            return reconstruct_path(current)
        if goal_function(current) == True:
            print("Goal found")
            return reconstruct_path(current)
        open_set.remove(current)
        for nbor in neighbor_function(current):
            if isinstance(nbor, list):
                nbor = tuple(nbor)

            d = distance_function(current, nbor) # Distance from current to nbor
            tentative_gScore = g_score[current] + d # Distance from start to nbor
            g_score.setdefault(nbor, float('inf'))
            if tentative_gScore < g_score[nbor]:
                # This path to nbor is better than any previous one. Record it!
                came_from[nbor] = current
                g_score[nbor] = tentative_gScore
                f_score[nbor] = tentative_gScore + heuristic_function(nbor)
                if nbor not in open_set:
                    open_set.append(nbor)
        iterations += 1
    return []

def solve(input_state, goal_function, distance_function, heuristic_function, neighbor_function, depth=None):
    path = solve_internal(input_state, goal_function, distance_function, heuristic_function, neighbor_function, depth)
    print(input_state)
    print(path[-2])
    for i in range(9):
        if int(input_state[i]) == 0 and int(path[-2][i]) == 2:
            return i
    return None
