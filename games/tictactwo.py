
class TicTacTwo:
    TURN_INDEX = 0

    def __init__(self, board=None):
        self.TURN_INDEX = 0
        if board is not None:
            self.board = board
        else:
            self.board = [
                1, # who's turn is it?

                # the board (0 is nothing there, 1 is player 1s cell, 2 is player 2s cell)
                0, 0, 0,
                0, 0, 0,
                0, 0, 0
            ]
    
    def run_once(self, input_function, kwargs):
        selected_input = input_function(**kwargs)


        if self.board[selected_input] == 0:
            temp = list(self.board)
            temp[selected_input] = self.board[self.TURN_INDEX] # change the selected input to the players
            self.board = tuple(temp)
            return True
        else:
            print("bad move")
            return False
    
    def change_turn(self):
        self.board[self.TURN_INDEX] = 3 - self.board[self.TURN_INDEX] # flip the turn

    def print(self):
        print(self.board)

    def get_board(self):
        return self.board


def get_human_input(prompt):
    valid_input = False
    while not valid_input:
        try:
            choice = int(input(prompt))
        except ValueError as e:
            print("Please provide a number between 1 and 9 to choose which box to play.")
            continue
        
        if choice in range(1, 10):
            valid_input = True
        else:
            print("Please provide a number between 1 and 9 to choose which box to play.")
        
    return choice



def isP(val, player):
    return int(val) == player

def check_win(state, p):
    # Horizontal
    if isP(state[1], p) and isP(state[2], p) and isP(state[3], p):
        return True
    if isP(state[4], p) and isP(state[5], p) and isP(state[6], p):
        return True
    if isP(state[7], p) and isP(state[8], p) and isP(state[9], p):
        return True
    # Vertical
    if isP(state[1], p) and isP(state[4], p) and isP(state[7], p):
        return True
    if isP(state[2], p) and isP(state[5], p) and isP(state[8], p):
        return True
    if isP(state[3], p) and isP(state[6], p) and isP(state[9], p):
        return True
    # Diagonal
    if isP(state[1], p) and isP(state[5], p) and isP(state[9], p):
        return True
    if isP(state[3], p) and isP(state[5], p) and isP(state[7], p):
        return True
    # No win
    return False

def check_draw(state):
    for i in range(1, 10):
        if state[i] == 0:
            return False
    return True

def find_steps(state):
    states = []
    for i in range(1, 10):
        if state[i] == 0:
            simulated_board = TicTacTwo(state)
            simulated_board.run_once(
                input_function=lambda: i,
                kwargs={}
            )
            new_state = simulated_board.get_board()
            states.append(new_state)
    return states