
import generic_pathfind.astar as gpf
import games.tictactoe as tictactoe


def main():
    tictactoe.start_game(ai=gpf.solve)




if __name__ == '__main__':
    main()
