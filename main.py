from random import choice

import generic_pathfind.astar as gpf
import generic_pathfind.depth_first as dfpf
import games.tictactoe as tictactoe
from games.tictactwo import TicTacTwo, get_human_input, check_win, check_draw, find_steps

def combination_func(values, args={}):
    version = 6
    decay = 1.0
    match version:
        case 0:
            # Max
            values.sort(key=lambda x: x[0])
            return values[-1][0] * decay, values[-1][1]
        case 1:
            # Min
            values.sort(key=lambda x: x[0])
            return values[0][0] * decay, values[0][1]
        case 2:
            # Average
            values.sort(key=lambda x: x[0])
            avg = sum(values[i][0] for i in range(len(values))) / len(values)
            return avg * 0.8, values[0][1]
        case 3:
            # Median
            values.sort(key=lambda x: x[0])
            return values[len(values)//2][0] * decay, values[len(values)//2][1]
        case 4:
            # Average of non-zero values
            nonzero = [x for x in values if x[0] != 0]
            avg = sum(x[0] for x in nonzero) / len(nonzero)
            nonzero.sort(key=lambda x: x[0])
            return avg * decay, nonzero[0][1]
        case 5:
            # Combination
            values.sort(key=lambda x: x[0])
            # Get avg of nonzero values
            no_draw = [x for x in values if x[0] != 0]
            avg2 = sum(no_draw[i][0] for i in range(len(no_draw))) / len(no_draw)
            val, _ = values[0]
            return (val + avg2) * decay, values[-1][1]
        case 6:
            # Min Max
            values.sort(key=lambda x: x[0])
            if args["depth"] % 2 == 0:
                return values[-1][0] * decay, values[-1][1] # Max
            else:
                return values[0][0] * decay, values[0][1] # Min
        case 7:
            # Can I win before opponent?
            values.sort(key=lambda x: x[0])
            # Fastest win
            val1, move1 = values[-1]
            # Fastes loss
            val2, move2 = values[0]
            return (val1 - val2) * decay, move1
        case _:
            # Random
            return choice(values)
            

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
    
    win_scale = 1.0
    lose_scale = 1.0

    is_final = False
    while not is_final:
        game.run_once(dfpf.solve, kwargs={
            "current_state": game.get_board(),
            "known_states": {
                # Win
                (1,
                 1,1,1,
                 0,0,0,
                 0,0,0) : (1 * win_scale, None),
                (1,
                 0,0,0,
                 1,1,1,
                 0,0,0) : (1 * win_scale, None),
                (1,
                 0,0,0,
                 0,0,0,
                 1,1,1) : (1 * win_scale, None),
                (1,
                 1,0,0,
                 1,0,0,
                 1,0,0) : (1 * win_scale, None),
                (1,
                 0,1,0,
                 0,1,0,
                 0,1,0) : (1 * win_scale, None),
                (1,
                 0,0,1,
                 0,0,1,
                 0,0,1) : (1 * win_scale, None),
                (1,
                 0,0,1,
                 0,1,0,
                 1,0,0) : (1 * win_scale, None),
                (1,
                 1,0,0,
                 0,1,0,
                 0,0,1) : (1 * win_scale, None),
                # Lose
                (2,
                 2,2,2,
                 0,0,0,
                 0,0,0) : (-1 * lose_scale, None),
                (2,
                 0,0,0,
                 2,2,2,
                 0,0,0) : (-1 * lose_scale, None),
                (2,
                 0,0,0,
                 0,0,0,
                 2,2,2) : (-1 * lose_scale, None),
                (2,
                 2,0,0,
                 2,0,0,
                 2,0,0) : (-1 * lose_scale, None),
                (2,
                 0,2,0,
                 0,2,0,
                 0,2,0) : (-1 * lose_scale, None),
                (2,
                 0,0,2,
                 0,0,2,
                 0,0,2) : (-1 * lose_scale, None),
                (2,
                 0,0,2,
                 0,2,0,
                 2,0,0) : (-1 * lose_scale, None),
                (2,
                 2,0,0,
                 0,2,0,
                 0,0,2) : (-1 * lose_scale, None)
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
