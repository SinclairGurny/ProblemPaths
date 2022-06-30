import random
from sklearn.ensemble import RandomForestClassifier

class EvalModel:
    def __init__(self, func_type: str):
        match func_type:
            case "random":
                self.version = -1
            case "max":
                self.version = 0
            case "min":
                self.version = 1
            case "avg":
                self.version = 2
            case "median":
                self.version = 3
            case "minimax":
                self.version = 6


    def choose(self, values, args={}):
        """
        Evaluates a list of (value, move) pairs and chooses the best one.
        Includes a variety of heuristics:
        Min, Max, Average, Median, Avg of NonZero, Minimax, Random, etc
        """
        if len(values) == 0:
            return 0, None
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