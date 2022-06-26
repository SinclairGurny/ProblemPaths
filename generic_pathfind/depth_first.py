"""
Generic Depth First Search Algorithm

solve_internal returns evaluation, state transition
memory: dict(state-like object -> (value, state transition))
contains_func(state, memory) -> index of state in known_states
evaluation_func(state, extra_info?) -> chooses from list of (evaluation, state transition), may take in extra information
transition_func(state) -> returns list of (state, state transition)

"""

import time

def solve_internal(
        current_state: tuple,
        memory: dict,
        contains_func,
        evaluation_func,
        transition_func,
        depth: int,
        max_depth: int):

    if isinstance(current_state, list):
        current_state = tuple(current_state)

    mem = contains_func(current_state, memory)
    if mem is not None:
        return mem

    if depth == 0:
        return 0, None

    possible_moves = transition_func(current_state)
    if len(possible_moves) == 0:
        return 0, None

    values = []
    for potential_move, move in possible_moves:
        # Recurse
        value, _ = solve_internal(potential_move, memory, contains_func, evaluation_func, transition_func, depth - 1, max_depth)
        values.append((value, move))

    choice = evaluation_func(values, {"depth": depth})

    # Debug
    if depth == max_depth:
        print("Evaluation of possible moves:\n  ", values)

    return choice

def solve(current_state: tuple,
          memory: dict,
          contains_func,
          evaluation_func,
          transition_func,
          max_depth: int):
    # Run solver
    start = time.time()
    _, transition = solve_internal(
        current_state,
        memory,
        contains_func,
        evaluation_func,
        transition_func,
        max_depth,
        max_depth
    )
    print("Solver took:", time.time() - start)
    # Return only the state transition
    return transition

