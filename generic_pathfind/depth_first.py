from copy import deepcopy

def solve_internal(current_state: tuple,
          known_states: dict,
        #   path: list,
          contains_function,
          combination_function,
          neighbor_function,
          depth: int,
          max_depth: int):
    #print("Starting solve_internal")
    if isinstance(current_state, list):
        current_state = tuple(current_state)

    index = contains_function(current_state, known_states.keys())
    if index is not None:
        return known_states[index]

    if depth == 0:
        return 0, None # reconsider this value later

    possible_moves = neighbor_function(current_state)
    if len(possible_moves) == 0:
        #print(current_state)
        return 0, None # reconsider this value later

    values = []
    for potential_move, move in possible_moves:
        value, _ = solve_internal(potential_move, known_states, contains_function, combination_function, neighbor_function, depth - 1, max_depth)
        values.append((value, move))
    
    choice = combination_function(values, {"depth": depth})
    if depth == max_depth:
        print('finishing')
        print("current_state: " + str(current_state))
        print("choice: " + str(choice))
        print("values: " + str(values))
        
    return choice



def solve(current_state: tuple,
          known_states: dict,
          contains_function,
          combination_function,
          neighbor_function,
          depth: int):
    # print("Starting solve")
    val, move = solve_internal(
        current_state,
        known_states,
        contains_function,
        combination_function,
        neighbor_function,
        depth,
        depth
    )
    # print("Finishing solver")
    # print(val, move)
    return move

"""
known_states = {
    goal states x -> numerical 'value' or 'weight' of the state
    x : (fitness_function(x), move)
}
"""

