import time


# TODO add caching of states
def solve_internal(current_state: tuple, memory, evaluator, depth: int, max_depth: int):

    evals = memory.retrieve_evals(current_state)
    if len(evals) > 0:
        return evals[0], None

    if depth == 0:
        return 0, None

    transitions = memory.retrieve_transitions(current_state)
    if len(transitions) == 0:
        return 0, None

    values = []
    for transition_vector in transitions:
        # Recurse
        assert(len(transition_vector) == len(current_state))
        new_state = tuple(current_state[i] + transition_vector[i] for i in range(len(current_state)))
        value, _ = solve_internal(new_state, memory, evaluator, depth - 1, max_depth)
        values.append((value, transition_vector))

    choice = evaluator.choose(values, {"depth": depth})

    # Debug
    if depth == max_depth:
        print("Evaluation of possible moves:\n  ", values)

    return choice


def Solver(current_state: tuple,
          memory: dict,
          evaluator,
          max_depth: int):
    # Run solver
    start = time.time()
    _, transition = solve_internal(
        current_state,
        memory,
        evaluator,
        max_depth,
        max_depth
    )
    print("Solver took:", time.time() - start)
    # Return only the state transition
    return transition

