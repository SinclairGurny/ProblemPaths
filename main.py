import generic_pathfind.depth_first as dfpf
from games.tictactwo import TicTacTwo, find_transitions, get_human_input, check_win, check_draw, find_transitions
from models.tttmodel import get_memory, compare, evaluation


def main():
    # tictactoe.start_game(ai=gpf.solve)
    game = TicTacTwo()
    
    ai_player_starts = True
    
    print("Starting game...")
    game.print(False)

    while True:
        print("\n")
        if ai_player_starts: # Skip AI's first turn
            game.run_once(dfpf.solve, kwargs={
                "current_state": game.get_board(),
                "memory": get_memory(),
                "contains_func": compare,
                "evaluation_func": evaluation,
                "transition_func": find_transitions,
                "max_depth": 10
            })
            game.print(False)

            if check_win(game.get_board(), 1):
                print("player 1 wins!")
                break

            if check_win(game.get_board(), 2):
                print("player 2 wins!")
                break

            if check_draw(game.get_board()):
                print("Draw!")
                break

        game.change_turn()
        game.run_once(get_human_input, kwargs={"prompt": "Move: "})
        game.print(False)

        if check_win(game.get_board(), 1):
            print("player 1 wins!")
            break

        if check_win(game.get_board(), 2):
            print("player 2 wins!")
            break

        if check_draw(game.get_board()):
            print("draw!")
            break
        
        game.change_turn()
        ai_player_starts = True





if __name__ == '__main__':
    main()
