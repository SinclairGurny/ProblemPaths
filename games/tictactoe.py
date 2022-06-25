"""
Implements the game tic tac toe.
"""
from copy import deepcopy

start = [1, # Use one dimension for turn
         0, 0, 0,
         0, 0, 0,
         0, 0, 0]

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

def difference(state1, state2):
    count = 0
    for i in range(1, 10):
        if state1[i] != state2[i]:
            count += 1
    return count

def distance_to_goal_simple(state):
    # Win = 1, Lose = -1, Else = 0
    if check_win(state, 1):
        return 1
    elif check_win(state, 2):
        return 100000
    else:
        return 0
    
def play_move(state, move):
    new_state = deepcopy(state)
    player = int(new_state[0]) # Get player
    new_state[move] = float(player) # Play move
    new_state[0] = 3 - player # Switch player
    return new_state

def distance_to_goal_advanced(state):
    # Think one move in advance
    curr_player = int(state[0])
    if check_win(state, curr_player):
        return 1
    elif check_win(state, 3 - curr_player):
        return 1000
    else:
        for i in range(1, 10):
            new_state = play_move(list(state), i)
            if check_win(new_state, curr_player):
                return 1
        return 0

def find_steps(state):
    states = []
    for i in range(1, 10):
        if state[i] == 0:
            new_state = play_move(list(state), i)
            states.append(new_state)
    return states

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


# ====== Start game ============================
def start_game(ai=None):
    my_state = deepcopy(start)

    while True:
        print("\nCurrent state:")
        print(f"Player {my_state[0]}'s turn")
        print(my_state[1:4], "= 1, 2, 3")
        print(my_state[4:7], "= 4, 5, 6")
        print(my_state[7:10], "= 7, 8, 9")
        if check_win(my_state, 1):
            print("Player 1 wins!")
            break
        elif check_win(my_state, 2):
            print("Player 2 wins!")
            break
        elif check_draw(my_state):
            print("Draw!")
            break
        turn = int(my_state[0])
        if turn == 1:
            # Player 1 turn
            loc = get_human_input("Player 1, choose your move: ")
            my_state = play_move(my_state, int(loc))
        else:
            # AI or Player 2
            print(str(ai))
            if ai is not None:
                ai_move = ai(
                    my_state, # State
                    lambda state: check_win(state, 2), # Goal
                    lambda state1, state2: difference(state1, state2), # Distance
                    lambda state: distance_to_goal_advanced(state), # Heuristic
                    lambda state: find_steps(state), # Steps
                    None # Depth
                )
                print("Ai playing: ", ai_move)
                my_state = play_move(my_state, ai_move)
                print("Beep boop")
            else:
                loc = get_human_input("Player 2, choose your move: ")
                my_state = play_move(my_state, int(loc))
