"""
Implements the functions necessary for Tic Tac Toe
"""


class TicTacToo:
    TURN_INDEX = 0

    def __init__(self, board=None):
        self.TURN_INDEX = 0
        if board is not None:
            self.board = board
        else:
            self.board = (
                1, # who's turn is it?
                # the board (0 is nothing there, 1 is player 1s cell, 2 is player 2s cell)
                0, 0, 0,
                0, 0, 0,
                0, 0, 0
            )
    
    def run_once(self, input_function, kwargs):
        selected_input = input_function(**kwargs)
        assert self.board[selected_input] == 0, "Invalid move!"
        temp = list(self.board)
        temp[selected_input] = self.board[self.TURN_INDEX] # change the selected input to the players
        self.board = tuple(temp)
        turn = self.board[self.TURN_INDEX]
        self.change_turn()
        return turn, selected_input
    
    def run_ai(self, move):
        selected_input = move
        assert self.board[selected_input] == 0, "Invalid move!"
        temp = list(self.board)
        temp[selected_input] = self.board[self.TURN_INDEX] # change the selected input to the players
        self.board = tuple(temp)
        turn = self.board[self.TURN_INDEX]
        self.change_turn()
        return turn, selected_input
    
    def change_turn(self):
        temp = list(self.board)
        temp[self.TURN_INDEX] = 3 - self.board[self.TURN_INDEX] # flip the turn
        self.board = tuple(temp)

    def print(self, include_turn=True):
        print("Current state:")
        if include_turn:
            print(f"Player {self.board[0]}'s turn")
        print(self.board[1:4], "= 1, 2, 3")
        print(self.board[4:7], "= 4, 5, 6")
        print(self.board[7:10], "= 7, 8, 9")

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


def check_win(state, p):
    """Checks for a win for player p in state"""
    isP = lambda val, player: int(val) == player
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
    """Checks for draw, assuming that no one has won"""
    for i in range(1, 10):
        if state[i] == 0:
            return False
    return True
