from copy import deepcopy

def solve(current_state: tuple,
          known_states: dict,
        #   path: list,
          combination_function,
          neighbor_function,
          depth: int):
    if isinstance(current_state, list):
        current_state = tuple(current_state)

    if current_state in known_states.keys():
        return known_states[current_state]

    if depth == 0:
        return 0, None # reconsider this value later

    possible_moves = neighbor_function(current_state)
    if len(possible_moves) == 0:
        return -2, None # reconsider this value later

    values = []
    for potential_move in possible_moves:
        value, moves = solve(potential_move, known_states, combination_function, neighbor_function, depth - 1)
        values.append((value, moves))
    
    return combination_function(values)



# def solve(current_state: tuple,
#           known_states: dict,
#           path: list,
#           combination_function,
#           neighbor_function,
#           depth: int):
#     something = solve_internal(current_state,
#                                known_states,
#                                path,
#                                combination_function,
#                                neighbor_function,
#                                depth)

"""
known_states = {
    goal states x -> numerical 'value' or 'weight' of the state
    x : (fitness_function(x), move)
}
"""