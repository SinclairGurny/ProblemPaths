import random
from time import time

from modules.memory import MemoryModule
from modules.search import Solver
from models.evalmodel import EvalModel

from games.tictactoe_v3 import TicTacToo as TicTacToe
from games.tictactoe_v3 import get_human_input, check_win, check_draw

def convert_to_transition(turn, move):
    turn_val = 1 if turn == 1 else -1
    move_val = 1 if turn == 1 else 2
    vec = [turn_val, 0,0,0, 0,0,0, 0,0,0]
    vec[move] = move_val
    return tuple(vec)

def transition_to_move(state, transition):
    move = -1
    for i in range(1, 10):
        if transition[i] > 0:
            move = i
            break
    if move == -1:
        return -1
    if state[move] == 0:
        return move
    else: 
        return -1
    
def find_random_move(state):
    moves = []
    for i in range(1, 10):
        if state[i] == 0:
            moves.append(i)
    return random.choice(moves)

def train(memory, iters=100):
    for i in range(iters):
        print(f"Running game {i} : ", end="")
        # Create game
        game=TicTacToe()
        while True:
            # Player 1
            last_pos = game.get_board()
            rand_move = find_random_move(last_pos)
            turn, move = game.run_ai(rand_move)
            memory.store(last_pos, transition=convert_to_transition(turn, move))
            
            # Check for win
            if check_win(game.get_board(), 1):
                print("player 1 wins!", game.get_board())
                memory.store(game.get_board(), eval=1)
                break

            if check_win(game.get_board(), 2):
                print("player 2 wins!", game.get_board())
                memory.store(game.get_board(), eval=-1)
                break

            if check_draw(game.get_board()):
                print("Draw!", game.get_board())
                memory.store(game.get_board(), eval=0)
                break

def main():
    # Init solver
    memory = MemoryModule()
    evaluator = EvalModel("minimax")
    
    # Train
    start = time()
    train(memory, iters=200)
    print("Training took: ", time() - start)
    
    # TODO: add serialization of memory
    
    # Init game
    while True:
        game = TicTacToe()
        
        print("Starting game...")
        display_turn = True
        game.print(display_turn)
        
        # Play game
        while True:
            print("\n")
            last_pos = game.get_board()
            ai_transition = Solver(game.get_board(), memory, evaluator, 4)
            if ai_transition is None or transition_to_move(last_pos, ai_transition) == -1:
                print("No move found!")
                turn, move = game.run_once(get_human_input, kwargs={"prompt": "Move: "})
                memory.store(last_pos, transition=convert_to_transition(turn, move))
            else:
                ai_move = transition_to_move(last_pos, ai_transition)
                print(f"AI move: {ai_transition} -> {ai_move}")
                turn, move = game.run_ai(ai_move)
                memory.store(last_pos, transition=convert_to_transition(turn, move))
                
            game.print(display_turn)
            
            # Check for win
            if check_win(game.get_board(), 1):
                memory.store(game.get_board(), eval=1)
                print("player 1 wins!")
                break

            if check_win(game.get_board(), 2):
                memory.store(game.get_board(), eval=-1)
                print("player 2 wins!")
                break

            if check_draw(game.get_board()):
                memory.store(game.get_board(), eval=0)
                print("Draw!")
                break
            
            last_pos = game.get_board()
            turn, move = game.run_once(get_human_input, kwargs={"prompt": "Move: "})
            memory.store(last_pos, transition=convert_to_transition(turn, move))
            game.print(display_turn)

            if check_win(game.get_board(), 1):
                memory.store(game.get_board(), eval=1)
                print("player 1 wins!")
                break

            if check_win(game.get_board(), 2):
                memory.store(game.get_board(), eval=-1)
                print("player 2 wins!")
                break

            if check_draw(game.get_board()):
                memory.store(game.get_board(), eval=0)
                print("draw!")
                break



if __name__ == '__main__':
    main()