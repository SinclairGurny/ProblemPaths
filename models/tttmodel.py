import random

def evaluation(values, args={}):
    """
    Evaluates a list of (value, move) pairs and chooses the best one.
    Includes a variety of heuristics:
    Min, Max, Average, Median, Avg of NonZero, Minimax, Random, etc
    """
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
            return random.choice(values)
            

def compare(current_state, memory):
    """Compares current state to memory and returns a list of (value, move) pairs"""
    for state, info in memory.items():
        if len(current_state) == len(state):
            match=True
            for i in range(1, len(state)):
                if state[i] == 0:
                    continue
                if current_state[i] != state[i]:
                    match=False
            if match:
                return info
        else:
            raise IndexError("parallel tuples do not have the same length, they cannot be iterated over simultaneously.")
    return None

def get_memory(config: dict = {}):
    win_scale = 1.0
    lose_scale = 1.0
    if "win_scale" in config:
        win_scale = config["win_scale"]
    if "lose_scale" in config:
        lose_scale = config["lose_scale"]
    memory = {
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
    }
    return memory