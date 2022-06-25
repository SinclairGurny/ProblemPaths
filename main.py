
from itertools import combinations
import generic_pathfind.astar as gpf
import generic_pathfind.depth_first as dfpf
import games.tictactoe as tictactoe
from games.tictactwo import TicTacTwo, get_human_input, check_win, check_draw, find_steps

def combination_func(values):
    values.sort(key=lambda x: x[0])
    return values[-1]

def compare(current_state, known_states):
    for state in known_states:
        if len(current_state) == len(state):
            match=True
            for i in range(1, len(state)):
                if state[i] == 0:
                    continue
                if current_state[i] != state[i]:
                    match=False
            if match:
                return state
        else:
            raise IndexError("parallel tuples do not have the same length, they cannot be iterated over simultaneously.")
    return None

def main():
    # tictactoe.start_game(ai=gpf.solve)
    game = TicTacTwo()

    path = []

    is_final = False
    while not is_final:
        game.run_once(dfpf.solve, kwargs={
            "current_state": game.get_board(),
            "known_states": {
                (1,
                 1,1,1,
                 0,0,0,
                 0,0,0) : (1, None),
                (1,
                 0,0,0,
                 1,1,1,
                 0,0,0) : (1, None),
                (1,
                 0,0,0,
                 0,0,0,
                 1,1,1) : (1, None),
                (1,
                 1,0,0,
                 1,0,0,
                 1,0,0) : (1, None),
                (1,
                 0,1,0,
                 0,1,0,
                 0,1,0) : (1, None),
                (1,
                 0,0,1,
                 0,0,1,
                 0,0,1) : (1, None),
                (1,
                 0,0,1,
                 0,1,0,
                 1,0,0) : (1, None),
                (1,
                 1,0,0,
                 0,1,0,
                 0,0,1) : (1, None)
            },
            # "path": path,
            "contains_function": compare,
            "combination_function": combination_func,
            "neighbor_function": find_steps,
            "depth": 10
        })
        game.print()

        if check_win(game.get_board(), 1):
            print("player 1 wins!")
            is_final = True
            continue

        if check_win(game.get_board(), 2):
            print("player 2 wins!")
            is_final = True
            continue

        if check_draw(game.get_board()):
            print("draw!")
            is_final = True
            continue

        game.change_turn()
        game.run_once(get_human_input, kwargs={
            "prompt": "gimme: "
        })
        game.print()

        if check_win(game.get_board(), 1):
            print("player 1 wins!")
            is_final = True
            continue

        if check_win(game.get_board(), 2):
            print("player 2 wins!")
            is_final = True
            continue

        if check_draw(game.get_board()):
            print("draw!")
            is_final = True
            continue
        
        game.change_turn()





if __name__ == '__main__':
    main()
