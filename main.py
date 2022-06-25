
from itertools import combinations
import generic_pathfind.astar as gpf
import generic_pathfind.depth_first as dfpf
import games.tictactoe as tictactoe
from games.tictactwo import TicTacTwo, get_human_input, check_win, check_draw, find_steps

def combination_func(values):
    values.sort(key=lambda x: x[0])
    return values[0]

def main():
    # tictactoe.start_game(ai=gpf.solve)
    game = TicTacTwo()

    path = []


    while True:
        print("Loop")
        game.run_once(dfpf.solve, kwargs={
            "current_state": game.get_board(),
            "known_states": {
                (1,
                 1,1,1,
                 0,0,0,
                 0,0,0) : (1, None)
            },
            # "path": path,
            "combination_function": combination_func,
            "neighbor_function": find_steps,
            "depth": 10
        })
        game.print()
        input()




if __name__ == '__main__':
    main()
